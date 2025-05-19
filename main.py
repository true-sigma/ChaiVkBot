import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from config.settings import vk_api_key
from src.character_ai import chai
from src.json.json_tools import load_user_chats, save_user_chats


# Initialize VK API
def start_session():
    vk_session = vk_api.VkApi(token=vk_api_key)
    vk1 = vk_session.get_api()
    longpoll1 = VkLongPoll(vk_session, wait=30)
    return longpoll1, vk1

def main1(longpoll, vk):
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
            longpoll, vk = start_session()
            main1(longpoll, vk)
        except Exception as e:
            print(e)
            longpoll, vk = start_session()
            main1(longpoll, vk)

if __name__ == '__main__':
    main()
