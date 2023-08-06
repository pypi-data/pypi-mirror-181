mode_registry = {}

def register_mode(name):
  def decorator(cls):
    mode_registry[name] = cls
    return cls
  return decorator

def get_mode(name):
  return mode_registry[name]

@register_mode('base')
class BaseMode:

  username = ''
  visible = False

  seed = ''

  def __init__(self, state={}):
    pass

  def ask(self, text):
    yield ''

  def get_seed(self):
    return self.seed

  def set_seed(self, seed):
    self.seed = seed

  def rollback(self, message_id=''):
    pass

  def save(self):
    return {}

  def stats(self):
    return ''

  def print(self):
    print()

  # To use ipdb set:
  #   export PYTHONBREAKPOINT=IPython.terminal.debugger.set_trace
  def debug(self):
    breakpoint()
