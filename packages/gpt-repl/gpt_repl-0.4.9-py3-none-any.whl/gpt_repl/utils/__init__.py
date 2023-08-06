from itertools import chain

from .printer import printer
from .loader import Loader

def peek(gen):
  first = next(gen)
  return ( chain([ first ], gen), first )
