from itertools import chain

def peek(gen):
  first = next(gen)
  return ( chain([ first ], gen), first )
