import time

# from pychatgpt import Chat as PyChatGPT
# from pychatgpt.classes import chat as ChatHandler
# from pychatgpt.classes import openai as OpenAI

# from colorama import Fore

# class ChatBackend:

#   def __init__(self, email, password, conversation_id=None, previous_conversation_id=None):
#     self.email = email
#     self.password = password

#     self.conversation_id = conversation_id if conversation_id != "" else None
#     self.previous_conversation_id = previous_conversation_id if previous_conversation_id != "" else None

#     self.ChatGPT = PyChatGPT(
#       self.email,
#       self.password,
#       conversation_id=self.conversation_id,
#       previous_convo_id=self.previous_conversation_id
#     )
#     self.access_token = self.auth()


#   def auth(self):
#     return OpenAI.get_access_token()

#   def ask(self, text):
#     answer, previous_convo, convo_id = ChatHandler.ask(
#       auth_token=self.access_token,
#       prompt=text,
#       conversation_id=self.conversation_id,
#       previous_convo_id=self.previous_conversation_id,
#       proxies=''
#     )

#     if answer == "400" or answer == "401":
#         print(f"{Fore.RED}>> Failed to get a response from the API.")
#         return None

#     self.conversation_id = convo_id
#     self.previous_conversation_id = previous_convo

#     return answer.strip()



# from revChatGPT.revChatGPT import Chatbot


class ChatBackend:

  def __init__(self, email, password, conversation_id=None, previous_conversation_id=None):
    self.email = email
    self.password = password

    self.conversation_id = conversation_id if conversation_id != "" else None
    self.previous_conversation_id = previous_conversation_id if previous_conversation_id != "" else None


    # config = {
    #   "email": self.email,
    #   "password": self.password,
    # }
    # self.ChatGPT = Chatbot(
    #   config,
    #   conversation_id=self.conversation_id,
    # )

  def ask(self, text):
    time.sleep(.5)
    # response = self.ChatGPT.get_chat_response(text, output="text")

    # self.conversation_id = response["conversation_id"]
    # self.previous_conversation_id = response["parent_id"]

    # return response['message'].strip()

    self.conversation_id = 'conversation id'
    self.previous_conversation_id = 'previous conversation id'


#     return """
# ### This is some code:
# x
# y
# """

    return """
### This is some code:
and stuff

```
# Import the necessary modules
import sys

# Define a main() function
def main():

  # Print the message to the console
  print("Hello, world!")

# Call the main() function
main()
```
Such `wow`, most *amazing* **code** ,
asdf
"""
