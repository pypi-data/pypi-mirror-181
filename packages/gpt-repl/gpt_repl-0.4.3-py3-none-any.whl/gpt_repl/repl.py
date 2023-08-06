import prompt_toolkit as PromptToolkit
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.history import FileHistory
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.application.current import get_app
from prompt_toolkit import filters as Filters

from .utils import peek
from .config import Config
from .printer import printer

from .modes.synth_chat import SynthChatMode as ChatBackend
from .spinner import Spinner
from .commands import Commands

class REPL:

  def __init__(self, thread_id=None, config_path="~/.config/gpt_repl", autofills=[]):

    self.config = Config(config_path)
    self.thread = self.config.load_thread(thread_id)
    self.autofills = autofills
    self.Chat = None

  def run(self):
    self.warmup()
    self.Chat = ChatBackend( state=self.thread['state'] )

    print("Enter 'help' for a list of commands. Use Enter to submit and Tab to start a new line.\n")
    self.replay_thread()
    self.start_prompt_session()

    first_run = True

    while True:
      try:
        self.print_you_banner(len(self.thread["history"]) + 1)

        if len(self.autofills) == 0:
          text = self.prompt()
        else:
          text = self.autofills.pop(0)

        printer.print_markdown(text)

        if Commands.exec(self, text):
          continue

        self.thread["history"].append({
          "type": "you",
          "text": text,
        })

        # hack, will fix when I feel like it
        print('')
        if first_run:
          self.print_gpt_banner(len(self.thread["history"]) + 1)
          first_run = False
        else:
          self.print_gpt_banner(len(self.thread["history"]) + 1, stats=self.Chat.stats())

        with Spinner(show_timer=True, delay=1.5) as spinner:
          chat_data = peek(self.Chat.ask(text))[0]

        answer = ''
        with printer.live(transient=True) as screen:
          for data in chat_data:
            answer += data
            markdown = printer.to_markdown(answer.lstrip() + '█', code_theme='default')
            display_text = markdown.to_text() + '\n\n\n'
            screen.update(display_text)
        answer = answer.strip()

        printer.print_markdown(answer)
        print('')

        self.thread["history"].append({
          "type": "gpt",
          "text": answer,
        })

        self.save_thread()
      except (KeyboardInterrupt, EOFError):
        self.save_thread()
        printer.print_thread_closed(self.thread['id'])
        break

      except Exception as e:
        breakpoint()
        printer.print_thread_closed(self.thread['id'])
        raise e

  def start_prompt_session(self):
    self.session = PromptSession(
      erase_when_done=True,
      history=FileHistory(self.config.prompt_history_path),
    )
    self.kb = KeyBindings()

    @Filters.Condition
    def is_not_searching():
      return not get_app().layout.is_searching

    @self.kb.add('escape', 'enter', filter=is_not_searching)
    def _(event):
      event.current_buffer.insert_text('\n')
    @self.kb.add("tab", filter=is_not_searching)
    def _(event):
      prefix = event.current_buffer.document.leading_whitespace_in_current_line
      event.current_buffer.insert_text('\n' + prefix)
    @self.kb.add('enter', filter=is_not_searching)
    def _(event):
      if len(event.current_buffer.text.strip()) > 0:
        event.current_buffer.validate_and_handle()
      else:
        event.current_buffer.insert_text('\n')

  def prompt(self):
    text = self.session.prompt(
      '',
      multiline=True,
      key_bindings=self.kb,
      enable_open_in_editor=True,
      tempfile_suffix='.md',
    )
    return text.strip()

  def print_you_banner(self, count):
    printer.print_banner(
      bg_color='rgb(0,95,135)',
      text=' You:',
      prefix=f' {count} ',
      suffix=f' @{self.thread["id"]} [ synth-chat-mode ]'
    )

  def print_gpt_banner(self, count, stats=''):
    printer.print_banner(
      bg_color='spring_green4',
      text=' GPT:',
      prefix=f' {count} ',
      suffix=stats
    )

  def save_thread(self):
    if self.thread['id'] == None:
      return
    self.config.save_thread(self.thread['id'], {
      "id": self.thread['id'],
      "history": self.thread["history"],
      'state': self.Chat.save(),
    })

  def reset(self):
    self.thread = self.config.get_empty_thread(self.thread['id'])
    self.Chat = ChatBackend(state=self.thread['state'])
    self.save_thread()

  def replay_thread(self):
    for i, entry in enumerate(self.thread["history"]):
      if entry["type"] == "you":
        self.print_you_banner(i + 1)
      elif entry["type"] == "gpt":
        self.print_gpt_banner(i + 1)
      printer.print_markdown(entry["text"])
      print("")

  def warmup(self):
    messages = [ entry["text"] for entry in self.thread["history"] ] + self.autofills
    if any([ '```' in m for m in messages ]):
      with printer.print_thread_loading(self.thread['id']):
        printer.preload()
