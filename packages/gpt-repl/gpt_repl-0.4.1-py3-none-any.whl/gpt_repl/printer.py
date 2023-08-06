from colorama import Fore, Back, Style
from rich.console import Console
from rich.live import Live

from rich.text import Text

from .spinner import Spinner
from .markdown import SmartMarkdown, GuessLexer

rich_console = Console(color_system="truecolor", legacy_windows=False)

TrueColors = {

  "bg": {
    "blue": "\u001b[48;5;24m",
    "turquoise": "\u001b[48;5;29m",
    "red": "\u001b[48;5;88m"
  },

}

def render_markdown_to_html(text, title=''):
  svg = SmartMarkdown(f" \n{text}\n ", code_theme="monokai").to_svg(title=title)

  # The laziest hack ever
  svg = svg.replace('<g transform="translate(26,22)"', '<g transform="translate(-100,-100)"');
  svg = svg.replace('<rect fill="#292929"', '<rect fill="#000d1a"');

  return f"<div style=\"resize: horizontal; overflow: hidden; width: 1000px; height: auto;\">{svg}</div>"

class TempLog:

  def __init__(self, text=""):
    self.text = text

  def __enter__(self):
    print(f"\r{self.text}", end="")

  def __exit__(self, *args):
      print("\r" + " " * len(self.text), end="")
      print("\r", end="")

class RichLive:

  def __init__(self, console, transient=False):
    self.console = console
    self.transient = transient

  def update(self, content):
    max_height = self.console.height - 1
    raw_text = '\n'.join(content.split('\n')[-max_height:])
    text = Text.from_ansi(raw_text)

    self.live_enter.update(text, refresh=True)

  def __enter__(self):
    self.live = Live(
      console=self.console,
      vertical_overflow="vertical",
      auto_refresh=False,
      transient=self.transient,
    )
    self.live_enter = self.live.__enter__()
    self.live_enter._redirect_stdout=False

    return self

  def __exit__(self, *args):
    self.live.__exit__(*args)

class Printer:

  def __init__(self):
    self.console = Console(color_system="truecolor")

  def preload(self):
    GuessLexer.load()

  def print(self, text):
    self.console.print(text)

  def to_markdown(self, text, preserve_softbreak=True, code_theme='monokai'):
    if preserve_softbreak:
      text = '  \n'.join(text.split('\n'))
    return SmartMarkdown(text, code_theme=code_theme)

  def print_markdown(self, *args, **kwargs):
    self.console.print(self.to_markdown(*args, **kwargs))

  def print_banner(self, text, bg_color, prefix=""):
    color_code = TrueColors["bg"][bg_color]
    formatted_text = f"\u001b[48;5;236m\u001b[38;5;249m{prefix}{Fore.WHITE}\x1b[1m{color_code}{text}"

    print(f"{formatted_text}\u001b[K{Style.RESET_ALL}")

  def print_thread_loading(self, thread_id):
    return TempLog(f"Loading \x1b[1m@{thread_id}{Style.RESET_ALL}...")

  def print_thread_closed(self, thread_id):
    print(f"\nLeaving \x1b[1m@{thread_id}{Style.RESET_ALL}")

  def live(self, transient=False):
    return RichLive(self.console, transient=transient)

printer = Printer()
