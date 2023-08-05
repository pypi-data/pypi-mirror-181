# Adapted from https://github.com/rawandahmad698/PyChatGPT/blob/master/src/pychatgpt/classes/spinner.py

from itertools import cycle
import threading
import time, sys, math

# parts = '▁ ▂ ▃ ▄ ▅ ▆ ▅ ▄ ▃ ▁'.split(' ')
parts = '▁ ▂ ▃ ▄ ▅ ▆ ▅ ▄ ▃ ▁'.split(' ')
parts = [ '▁' ] * len(parts) + parts
frames = [
  ' '.join((parts[offset:] + parts[:offset])[:int(len(parts) / 2)])

  # ' '.join(parts[offset:] + parts[:offset])
  for offset in reversed(range(len(parts)))
]

class Spinner:

    def __init__(self, show_timer=False):
        self.show_timer = show_timer
        self.__screen_lock = threading.Event()
        self.__spinner = cycle(frames)
        self.__stop_event = False
        self.__thread = None

    def __enter__(self):
      self.start()

    def __exit__(self, *args):
      self.stop()

    def start(self):
        start_time = time.time()
        self.__stop_event = False

        def run_spinner():
            while not self.__stop_event:
                if self.show_timer:
                    print(f"\r[ {math.floor(time.time() - start_time)}s ] {next(self.__spinner)}  ", end="")
                else:
                    print(f"\r{next(self.__spinner)}  ", end="")
                time.sleep(0.05)

            self.__screen_lock.set()

        self.__thread = threading.Thread(target=run_spinner, args=(), daemon=True)
        self.__thread.start()

    def stop(self):
        self.__stop_event = True
        if self.__screen_lock.is_set():
            self.__screen_lock.wait()
            self.__screen_lock.clear()
        print("\r                                              ", end="")
        print("\r", end="")
