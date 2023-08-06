import os, openai, importlib, re, sys

# Needed to silence obnoxious logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

# Loaded lazily in `load_tokenizer`
# from transformers import GPT2TokenizerFast

class GPT3:

  def __init__(self, model='text-davinci-003', temperature=0.7):
    if not os.environ.get('OPENAI_API_KEY'):
      print("Please set the OPENAI_API_KEY environment variable. If you don't have one you can generate one here https://beta.openai.com/account/api-keys")
      sys.exit(0)

    self.model = model
    self.temperature = temperature
    self.tokenizer = None

  # transformers loads slowly because it depends on tensorflow. Load it lazily.
  def load_tokenizer(self):
    if self.tokenizer != None:
      return
    Tokenizer = importlib.import_module('transformers').GPT2TokenizerFast
    self.tokenizer = Tokenizer.from_pretrained('gpt2')

  def count_tokens(self, text, approximate=False, normalize=True):
    # GPT-3 uses Codex's tokenizer which handles whitespace better. To roughly
    # compensate for those changes, we can collapse all consecutive whitespace
    # into one space.
    if normalize:
      text = re.sub(r'[ \t]+', ' ', text)

    # Approximation recommended by OpenAI
    if approximate:
      return int(len(text) / 4)

    self.load_tokenizer()
    return len(self.tokenizer.tokenize(text, max_length=10000, truncation=True))

  def complete(self, *args, **kwargs):
    if kwargs.get('stream', False):
      return self.__complete_async(*args, **kwargs)
    else:
      return self.__complete_sync(*args, **kwargs)

  def __complete_sync(self, *args, **kwargs):
    kwargs['stream'] = False
    response = self.get_response(*args, **kwargs)
    return response.choices[0].text

  def __complete_async(self, *args, **kwargs):
    kwargs['stream'] = True
    response = self.get_response(*args, **kwargs)
    for data in response:
      yield data.choices[0].text

  def get_response(self, prompt, max_length=1000, stop=None, stream=False):
    return openai.Completion.create(
      engine=self.model,
      prompt=prompt,
      max_tokens=max_length,
      temperature=self.temperature,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      stop=stop,
      stream=stream,
      # logit_bias={
      #   '2949': 1, # Make "No" a more common token
      #   '44651': 1, # Make "Invalid" a more common token
      # },
    )

  def warm(self):
    return self.tokenizer != None
