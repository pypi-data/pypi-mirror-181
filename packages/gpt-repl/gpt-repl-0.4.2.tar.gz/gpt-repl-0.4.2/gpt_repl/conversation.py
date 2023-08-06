import math

class ConversationEngine:

  def __init__(self, completer, stream=True):
    self.completer = completer
    self.stream = stream

    self.bio = 'Delphi AI is a genius AI assistant that can help with literally anything, especially programming and math'

    self.conversation = []
    self.summaries = []
    self.recent_conversation = [
      {
        'from': 'server',
        'text': "Hey, need help with something?",
      },
      {
        'from': 'client',
        'text': "I've got a bunch of things I think you can help me with. Make sure to structure your responses.",
      },
      {
        'from': 'server',
        'text': "Cool, I'll do anything I can to help. Let's get started. I'll make sure to structure my responses ."
      },
    ]

    self.max_summaries = 8
    self.min_chunk_size = 200
    self.soft_max_message_size = 150

    self.max_response_length = 750
    self.max_prompt_length = 4000
    self.soft_max_prompt_length = 2000

  def save(self):
    return {
      'initialized': True,
      'summaries': self.summaries,
      'recent_conversation': self.recent_conversation
    }
    pass

  def load(self, data):
    self.summaries = data['summaries']
    self.recent_conversation = data['recent_conversation']

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
    self.condense_conversation(self.max_response_length)

    conversation_prompt = self.format_conversation_prompt(self.recent_conversation)
    return self.completer.create(
      conversation_prompt,
      max_length=self.max_response_length,
      stop=[ 'Adam:' ],
      stream=self.stream
    )

  def condense_conversation(self, space_required):
    for (i, msg) in enumerate(self.recent_conversation[:-8]):
      if self.has_target_prompt_size():
        break
      if self.count_tokens(msg['text']) > self.soft_max_message_size:
        print('shrinking message')
        msg['text'] = '( ' + self.completer.create(
          '\n'.join([
            'Purpose: You are a brilliant polymath AI assistant named Delphi AI helping your friend Adam over chat.',
            self.format_message(msg),
            f'Boss: Briefly summarize the previous message from {"you" if msg["from"] == "server" else "Adam"}, written as if you were {"Delphi AI" if msg["from"] == "server" else "Adam"}. Should be short and dense but informative. Use the past tense.',
            'Delphi AI:',
          ]),
          stop=[ 'Adam:' ],
        ).strip() + ' )'

    # while self.get_conversation_space() <= space_required or len(self.recent_conversation) >= 14:
    while self.get_conversation_space() <= space_required or len(self.recent_conversation) >= 18:
      if self.has_target_prompt_size():
        break

      print('condensing conversation')

      chunk = []
      chunk_text = ''
      while self.count_tokens(chunk_text) < self.min_chunk_size and len(self.recent_conversation) > 2:
        chunk += self.recent_conversation[:1]
        self.recent_conversation = self.recent_conversation[1:]
        chunk_text = '\n'.join([ m['text'] for m in chunk ])

      if len(chunk) == 0:
        breakpoint()
        raise 'hmm'

      summary_prompt = self.format_summary_prompt(chunk)
      response = 'Adam ' + self.completer.create(
        summary_prompt,
        # max_length=self.max_response_length,
        stop=[ 'Adam:' ]
      )

      self.summaries = self.summaries[-(self.max_summaries - 1):] + [ response.strip() ]

  def get_prompt_size(self):
    conversation_prompt = self.format_conversation_prompt(self.recent_conversation)
    return self.count_tokens(conversation_prompt)


  def get_conversation_space(self):
    return self.max_prompt_length - self.get_prompt_size() - self.max_response_length

  def has_target_prompt_size(self):
    return self.count_tokens(self.format_conversation_prompt(self.recent_conversation)) <= self.soft_max_prompt_length;

  def get_notes(self):
    return [ f'- {s}' for s in self.summaries ]

  def format_summary_prompt(self, messages, whitespace='\n'):
    return whitespace.join([
      self.bio,
      '# Recent Chat Conversation with Adam:',
      # *[ self.format_message(m) for m in messages ],
      '\n-----\n'.join([ self.format_message(m) for m in messages ]),
      'Boss: Give me your personal notes on the conversation. Should be terse but informative.',
      'Delphi AI: Adam'
    ])

  def format_conversation_prompt(self, messages, whitespace='\n'):
    return whitespace.join([
      self.bio,
      '# Delphi AI\'s Notes on conversation with Adam:',
      '- Adam demanded I give highly structured answers formatted in Markdown (lists like "1.", headers like "# title", code blocks like ```js etc)!',
      *self.get_notes(),
      '# Recent Chat Conversation with Adam:',
      # *[ self.format_message(m) for m in messages ],
      '\n-----\n'.join([ self.format_message(m) for m in messages ]),
      '-----\nDelphi AI:'
    ])

  def count_tokens(self, text):
    return self.completer.count_tokens(text)

  def format_message(self, message):
    if message['from'] == 'server':
      return f'Delphi AI: {message["text"]}'
    else:
      return f'Adam: {message["text"]}'

  def print(self, show_all=False):
    messages = self.conversation if show_all else self.recent_conversation
    # print(self.format_conversation_prompt(messages, whitespace='\n\n'))
    print(self.format_conversation_prompt(messages))
