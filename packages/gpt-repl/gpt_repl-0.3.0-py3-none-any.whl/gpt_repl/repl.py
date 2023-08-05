import pdb

import prompt_toolkit as PromptToolkit
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.history import FileHistory
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.application.current import get_app
from prompt_toolkit import filters as Filters

from .config import Config
from .printer import print_banner, print_markdown, print_thread_saved, print_thread_loading, preload, TempLog
from .chat_backend import ChatBackend
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
      email,
      password,
      conversation_id=self.thread["conversation_id"],
      previous_conversation_id=self.thread["previous_conversation_id"],
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

        print_markdown(text)

        if Commands.exec(self, text):
          continue

        self.thread["history"].append({
          "type": "you",
          "text": text,
        })

        print('')
        self.print_gpt_banner(len(self.thread["history"]) + 1)

        with Spinner(show_timer=True):
          answer = self.Chat.ask(text)
          preload()

        self.thread["history"].append({
          "type": "gpt",
          "text": answer,
        })

        print_markdown(answer)
        print('')

      except (KeyboardInterrupt, EOFError):
        if len(self.thread["history"]) > 0:
          self.save_thread()
          print_thread_saved(self.thread['id'])
        break

      except Exception as e:
        if len(self.thread["history"]) > 0:
          self.save_thread()
          print_thread_saved(self.thread['id'])
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
      event.current_buffer.validate_and_handle()

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
    print_banner(' You:', 'blue', prefix=f' {count} ')

  def print_gpt_banner(self, count):
    print_banner(' GPT:', 'turquoise', prefix=f' {count} ')

  def save_thread(self):
    if self.thread['id'] == None:
      return
    self.config.save_thread(self.thread['id'], {
      "id": self.thread['id'],
      "conversation_id": self.Chat.conversation_id,
      "previous_conversation_id": self.Chat.previous_conversation_id,
      "history": self.thread["history"],
    })

  def replay_thread(self):
    for i, entry in enumerate(self.thread["history"]):
      if entry["type"] == "you":
        self.print_you_banner(i + 1)
      elif entry["type"] == "gpt":
        self.print_gpt_banner(i + 1)
      print_markdown(entry["text"])
      print("")

  def warmup(self):
    messages = [ entry["text"] for entry in self.thread["history"] ] + self.autofills
    if any([ '```' in m for m in messages ]):
      with print_thread_loading(self.thread['id']):
        preload()
