import importlib

from rich.console import Console
from rich.markdown import Markdown, Paragraph, Heading, CodeBlock, BlockQuote, HorizontalRule, ListElement, ListItem, ImageItem

# The guesslang library loads quite slowly because of its dependency on TensorFlow,
# so we load it lazily using `importlib`
class GuessLexer:
  guess = None

  @classmethod
  def parse(cls, code):
    if code.strip() == '':
      return "text"
    try:
      GuessLexer.load()
      return GuessLexer.guess._language_map[GuessLexer.guess.language_name(code.strip())]
    except Exception as e:
      print(e)
      return "text"

  @classmethod
  def load(cls):
    if GuessLexer.guess == None:
      GuessLexer.guess = importlib.import_module('guesslang').Guess()

  @classmethod
  def warm(cls):
    self.load()
    GuessLexer.guess.language_name(' ')

class SmartCodeBlock(CodeBlock):
  @classmethod
  def create(cls, markdown, node):
    node_info = node.info or ""
    lexer_name = node_info.partition(" ")[0]

    if not lexer_name:
      lexer_name = GuessLexer.parse(str(node.literal))

    return cls(lexer_name or "text", markdown.code_theme)

class SmartMarkdown(Markdown):
  elements  = {
    "paragraph": Paragraph,
    "heading": Heading,
    "code_block": SmartCodeBlock,
    "block_quote": BlockQuote,
    "thematic_break": HorizontalRule,
    "list": ListElement,
    "item": ListItem,
    "image": ImageItem,
  }

  def to_html(self):
    console = Console(record=True)
    with console.capture() as capture:
      console.print(self)
    return console.export_html(inline_styles=True)

  def to_svg(self, title=''):
    console = Console(record=True)
    with console.capture() as capture:
      console.print(self)
    return console.export_svg(title=title)
