from src.json.json_tools import load_user_chats, save_user_chats
import vk_api
from config.settings import vk_api_key
from src.character_ai import chai
from vk_api.longpoll import VkLongPoll, VkEventType

# Initialize VK API
vk_session = vk_api.VkApi(token=vk_api_key)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session, wait=999999999) # implement correct wait

def main1():
    user_chats = load_user_chats()

    while True:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                user_id = str(event.user_id)

                if event.text.startswith("/"):
                    command = event.text.lower().split()[0]

                    if command == "/newchat":
                        # Create a new chat session
                        chat_id = chai.create_chat().chat_id
                        user_chats[user_id] = chat_id
                        save_user_chats(user_chats)
                        vk.messages.send(
                            user_id=user_id,
                            message="✅ Чат сброшен!",
                            random_id=0
                        )
                        print(f"Created new chat for user {user_id} with chat_id {chat_id}")

                else:
                    vk.messages.setActivity(user_id=user_id, type='typing', peer_id=event.peer_id)

                    if user_id not in user_chats:
                        chat_id = chai.create_chat().chat_id
                        user_chats[user_id] = chat_id
                        save_user_chats(user_chats)
                        print(f"Added new user {user_id} with chat_id {chat_id}")

                    chai_response = chai.get_chai_response(event.text, user_chats[user_id])
                    vk.messages.send(user_id=user_id, message=chai_response, random_id=0)

def main():
    while True:
        try:
            main1()
        except Exception as e:
            print(e)
            main()

if __name__ == '__main__':
    main()
