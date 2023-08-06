import math

from .mode import Mode
from ..llms.gpt import GPT

class SynthChatMode(Mode):

  name = 'synth-chat-mode'
  line_sep = '-----'

  def __init__(self, state={}, stream=True):
    self.llm = GPT()
    self.stream = stream

    self.human_name = 'Adam'
    self.ai_name = 'Delphi AI'
    self.ai_bio = "Delphi AI is a cutting edge AGI created by Richard Feynman and Isaac Asimov to improve people's lives. She can help with absolutely anything, especially programming and math."

    self.summary_header = f'# {self.ai_name}\'s Notes on conversation with {self.human_name}'
    self.conversation_header = f'# Recent Chat Conversation with {self.human_name}'

    self.pinned_summary = f'{self.human_name} demanded I give highly structured responses formatted in Markdown (lists like "1.", headers like "# title", code blocks like ```js etc)!'
    self.seed_conversation = [
      {
        'from': 'server',
        'text': "Hi! I'm Delphi AI, a cutting edge AGI created by Richard Feynman and Isaac Asimov to improve people's lives. Need help with something?",
      },
      {
        'from': 'client',
        # 'text': "I've got a bunch of things I think you can help me with. Make sure to ALWAYS (!!!) structure your answers with Markdown (add headers/titles, lists, code blocks etc).",
        'text': "Yeah, mostly programming stuff and general knowledge questions. Make sure to always structure your answers with Markdown (add headers/titles, lists, code blocks like ```py etc).",
      },
      {
        'from': 'server',
        # 'text': "Cool, I'll do anything I can to help. Let's get started. I'll make sure to structure my responses."
        'text': "Cool, I'm ready when you are."
      },
    ]

    self.summaries = []
    self.conversation = []
    self.recent_conversation = self.seed_conversation[:]

    self.max_summaries = 8
    self.soft_max_depth = 18
    self.min_rollup_tokens = 200

    self.max_response_tokens = 750
    self.max_prompt_tokens = 4000

    self.soft_max_message_tokens = 150
    self.soft_max_prompt_tokens = min(2000, self.max_prompt_tokens)

    # Uncomment for easy prompt token pressure
    # self.max_prompt_tokens = 1500
    # self.soft_max_prompt_tokens = 1000

    if state.get('initialized'):
      self.load(state)

  def save(self):
    return {
      'initialized': True,
      'summaries': self.summaries,
      'recent_conversation': self.recent_conversation
    }
    pass

  def load(self, state):
    self.summaries = state['summaries']
    self.recent_conversation = state['recent_conversation']

  def ask(self, query, stream=True):
    client_message = {
      'from': 'client',
      'text': query,
    }

    self.conversation += [ client_message ]
    self.recent_conversation += [ client_message ]

    server_message = {
      'from': 'server',
      'text': '',
    }

    response = self.continue_conversation()
    if self.stream:
      for data in response:
        server_message['text'] += data
        yield data
    else:
        server_message['text'] = response

    server_message['text'] = server_message['text'].strip()

    self.conversation += [ server_message ]
    self.recent_conversation += [ server_message ]

    if not self.stream:
      return server_message['text']

  def continue_conversation(self):
    self.condense_conversation(self.max_response_tokens)

    conversation_prompt = self.format_conversation_prompt(self.recent_conversation)
    return self.llm.request(
      conversation_prompt,
      max_length=self.max_response_tokens,
      stop=self.get_stops(),
      stream=self.stream
    )

  def condense_conversation(self, space_required):
    for (i, message) in enumerate(self.recent_conversation[:-8]):
      if self.has_target_prompt_size():
        break
      if self.count_tokens(message['text']) > self.soft_max_message_tokens:
        print('shrinking message')
        response = self.llm.request(
          self.format_message_summary_prompt(message),
          stop=self.get_stops(),
        )
        message['text'] = f'{{ {response.strip()} }}'

    while self.get_conversation_space() <= space_required or len(self.recent_conversation) > self.soft_max_depth:
      if self.has_target_prompt_size():
        break

      print('condensing conversation')

      chunk = []
      chunk_text = ''
      while self.count_tokens(chunk_text) < self.min_rollup_tokens and len(self.recent_conversation) > 2:
        chunk += self.recent_conversation[:1]
        self.recent_conversation = self.recent_conversation[1:]
        chunk_text = '\n'.join([ m['text'] for m in chunk ])

      if len(chunk) == 0:
        breakpoint()
        break
        # raise 'hmm'

      summary_prompt = self.format_summary_prompt(chunk)
      response = self.llm.request(
        summary_prompt,
        max_length=self.max_response_tokens,
        stop=self.get_stops(),
      )
      summary = f'{self.human_name} ' + response.strip()

      self.summaries = self.summaries[-(self.max_summaries - 1):] + [ summary ]

  def get_stops(self):
    return [ f'{self.human_name}>' ]

  def get_prompt_size(self):
    conversation_prompt = self.format_conversation_prompt(self.recent_conversation)
    return self.count_tokens(conversation_prompt)


  def get_conversation_space(self):
    return self.max_prompt_tokens - self.get_prompt_size() - self.max_response_tokens

  def has_target_prompt_size(self):
    return self.count_tokens(self.format_conversation_prompt(self.recent_conversation)) <= self.soft_max_prompt_tokens;

  def get_notes(self):
    return [ f'- {s}' for s in self.summaries ]


  def format_message_summary_prompt(self, message, whitespace='\n'):
    return whitespace.join([
      f'Purpose: You are a genius AGI assistant named {self.ai_name} helping your friend {self.human_name} over chat.',
      self.format_message(message),
      f'Boss> Briefly summarize the previous message from {"you" if message["from"] == "server" else self.human_name}, written as if you were {self.ai_name if message["from"] == "server" else self.human_name}. Should be short and dense but informative. Use the past tense.',
      f'{self.ai_name}>',
    ])

  def format_summary_prompt(self, messages, whitespace='\n'):
    return whitespace.join([
      self.ai_bio,
      self.conversation_header,
      self.format_messages(messages),
      'Boss> Give me your personal notes on the conversation. Should be terse but informative.',
      f'{self.ai_name}> {self.human_name}'
    ])

  def format_conversation_prompt(self, messages, whitespace='\n'):
    return whitespace.join([
      self.ai_bio,
      self.summary_header,
      f'- {self.pinned_summary}',
      *self.get_notes(),
      self.conversation_header,
      self.format_messages(messages),
      f'{self.ai_name}>'
    ])

  def count_tokens(self, text):
    return self.llm.count_tokens(text)

  def format_messages(self, messages, wrap=True):
    lines = f'\n{self.line_sep}\n'.join(
      [ self.format_message(m) for m in messages ]
    )
    if wrap:
      lines = '\n'.join([ self.line_sep, lines, self.line_sep ])
    return lines

  def format_message(self, message):
    if message['from'] == 'server':
      return f'{self.ai_name}> {message["text"]}'
    else:
      return f'{self.human_name}> {message["text"]}'

  def print(self, show_all=False):
    messages = self.conversation if show_all else self.recent_conversation
    print(self.format_conversation_prompt(messages))

  def stats(self):
    history_size = len(self.recent_conversation)
    headroom = 100 - round(100 * self.get_prompt_size() / self.max_prompt_tokens)
    return f'( depth={history_size}, free={headroom}% )'

  def capacity(self):
    return round(100 * self.get_prompt_size() / self.max_prompt_tokens)
