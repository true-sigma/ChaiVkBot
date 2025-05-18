from config.settings import chai_api_key, char
from characterai import pycai


client = pycai.Client(chai_api_key)
me = client.get_me()
chat = client.connect()

def create_chat():
    new, answer = chat.new_chat(char, me.id)
    return new

def get_chai_response(text, chat_id):
    message = chat.send_message(
        char, chat_id, text
    )

    return message.text