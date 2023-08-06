import click, os, datetime
from os.path import abspath

from .repl import REPL
from .config import Config

def load_file(file_path):
  with open(file_path) as f:
    text = f.read()
    return f"Provide a brief description of the following text:\n\n[ Loaded from {file_path} ]\n```\n{text}\n```"

@click.command()
@click.argument("cmd", type=str, required=False)
@click.option('-e', '--email', help="Email to use for login")
@click.option('-p', '--password', help="Password to use for login")
@click.option('-f', '--file', type=click.Path(exists=True), help="Path to text file to preload")
@click.option('-t', '--thread', default=None, help="Thread name to open")
@click.option('-c', '--config', default="~/.config/gpt_repl", help="Config directory")
@click.option('-l', '--list', is_flag=True, help="List all threads")
def run(cmd, email, password, file, thread, config, list):
  if list:
    list_threads(config)
    return

  if str(cmd)[0] == '@':
    thread = cmd[1:]

  autofills = []

  if file is not None:
    file_path = abspath(file)
    autofills.append(load_file(file_path))

  if thread == None:
    # thread = 'general'
    timestamp = datetime.datetime.now().strftime("%y-%m-%d_%H-%M-%S")
    thread = f"thread_{timestamp}"

  repl = REPL(
    email=email,
    password=password,
    thread_id=thread,
    config_path=config,
    autofills=autofills,
  )

  repl.run()

def list_threads(config_path):
  config = Config(config_path)
  threads = config.list_threads()
  for thread in threads:
    print(thread)

if __name__ == '__main__':
  run()
