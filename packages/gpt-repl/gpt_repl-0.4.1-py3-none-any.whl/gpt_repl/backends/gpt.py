from gpt_repl.conversation import ConversationEngine
import os, openai

# Needed to silence obnoxious logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

from transformers import GPT2TokenizerFast

# script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
# rel_path = "../prompts/builtin/assistant.txt"
# rel_path = "../prompts/builtin/programming.txt"
# abs_file_path = os.path.join(script_dir, rel_path)

class GPTBackend:

  # def __init__(self, email, password, conversation_id=None, previous_conversation_id=None):
  def __init__(self, internal={}):
    # This blog post claims code-davinci-002 has better performance than text-davinci-003
    # https://yaofu.notion.site/How-does-GPT-Obtain-its-Ability-Tracing-Emergent-Abilities-of-Language-Models-to-their-Sources-b9a57ac0fcf74f30a1ab9e3e36fa1dc1
    # self.engine = "code-davinci-002"

    self.engine = "text-davinci-003"
    # self.engine = "text-davinci-002"

    self.tokenizer = GPT2TokenizerFast.from_pretrained('gpt2')

    self.conversation = ConversationEngine(self, stream=True)
    if internal.get('initialized'):
      self.conversation.load(internal)

  def count_tokens(self, text):
    return len(self.tokenizer.tokenize(text, max_length=10000, truncation=True))

  def create(self, *args, **kwargs):
    if kwargs.get('stream', False):
      return self._createAsync(*args, **kwargs)
    else:
      return self._createSync(*args, **kwargs)

  def _createSync(self, *args, **kwargs):
    kwargs['stream'] = False
    response = self.get_response(*args, **kwargs)
    return response.choices[0].text

  def _createAsync(self, *args, **kwargs):
    kwargs['stream'] = True
    response = self.get_response(*args, **kwargs)
    for data in response:
      yield data.choices[0].text

  def get_response(self, prompt, max_length=1000, stop=[], stream=False):
    return openai.Completion.create(
      engine=self.engine,
      prompt=prompt,
      max_tokens=max_length,
      temperature=0.7,
      # temperature=0.5,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      stop=stop,
      stream=stream
    )

  def ask(self, text):
    return self.conversation.ask(text)

  def export(self):
    return self.conversation.save()

  # To use ipdb set:
  #   export PYTHONBREAKPOINT=IPython.terminal.debugger.set_trace
  def debug(self):
    breakpoint()

  def print(self, show_all=False):
    self.conversation.print(show_all)

  def billing(self):
    pass
