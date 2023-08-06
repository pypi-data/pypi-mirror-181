import pdb

import prompt_toolkit as PromptToolkit
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.history import FileHistory
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.application.current import get_app
from prompt_toolkit import filters as Filters

from .config import Config
from .printer import printer

# from .chat_backend import ChatBackend
from .backends.gpt import GPTBackend as ChatBackend
from .spinner import Spinner
from .commands import Commands

class REPL:

  def __init__(self, email="", password="", thread_id=None, config_path="~/.config/gpt_repl", autofills=[]):

    self.config = Config(config_path)
    self.thread = self.config.load_thread(thread_id)
    self.autofills = autofills

    self.ensure_auth(email, password)

  def ensure_auth(self, email, password):
    if not email or not password:
      (email, password) = self.config.get_auth()

    if not email or not password:
      print("Please enter your OpenAI account credentials:")
      email = PromptToolkit.prompt("Email: ")
      password = PromptToolkit.prompt("Password: ", is_password=True)
      print()

    self.config.set_auth(email, password)

  def run(self):
    self.warmup()

    print("Enter 'help' for a list of commands. Use Tab to start a new line.\n")

    (email, password) = self.config.get_auth()
    self.Chat = ChatBackend(
      # email,
      # password,
      internal=self.thread['internal']
      # conversation_id=self.thread["conversation_id"],
      # previous_conversation_id=self.thread["previous_conversation_id"],
    )

    self.replay_thread()
    self.start_prompt_session()

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

        print('')
        self.print_gpt_banner(len(self.thread["history"]) + 1)

        answer = ''
        with printer.live(transient=True) as screen:
          for data in self.Chat.ask(text):
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
    printer.print_banner(' You:', 'blue', prefix=f' {count} ')

  def print_gpt_banner(self, count):
    printer.print_banner(' GPT:', 'turquoise', prefix=f' {count} ')

  def save_thread(self):
    if self.thread['id'] == None:
      return
    self.config.save_thread(self.thread['id'], {
      "id": self.thread['id'],
      "history": self.thread["history"],
      'internal': self.Chat.export(),
    })

  def reset_thread(self):
    self.thread = self.config.get_empty_thread(self.thread['id'])
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
