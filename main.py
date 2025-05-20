import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from config.settings import vk_api_key, chai_api_key
from src.character_ai import chai
from src.json.json_tools import load_user_chats, save_user_chats


def check_credentials():
    """Validate that required API keys are present"""
    if not vk_api_key or not chai_api_key:
        raise ValueError("Missing credentials in settings file. Please provide both VK and Chai API keys.")


def initialize_vk():
    """Initialize and return VK API session objects"""
    try:
        vk_session = vk_api.VkApi(token=vk_api_key)
        vk = vk_session.get_api()
        longpoll = VkLongPoll(vk_session, wait=30)
        return longpoll, vk
    except vk_api.AuthError as e:
        raise ConnectionError(f"VK authentication failed: {e}")
    except Exception as e:
        raise ConnectionError(f"VK initialization error: {e}")


def handle_message(event, vk, user_chats):
    """Process incoming message and send response"""
    user_id = str(event.user_id)

    if event.text.startswith("/"):
        return handle_command(event, vk, user_id, user_chats)

    # Regular message processing
    vk.messages.setActivity(user_id=user_id, type='typing', peer_id=event.peer_id)

    if user_id not in user_chats:
        create_new_chat(user_id, user_chats)

    try:
        chai_response = chai.get_chai_response(event.text, user_chats[user_id])
        vk.messages.send(user_id=user_id, message=chai_response, random_id=0)
    except Exception as e:
        print(f"Error getting Chai response: {e}")
        vk.messages.send(
            user_id=user_id,
            message="⚠️ Произошла ошибка при обработке вашего сообщения. Попробуйте еще раз.",
            random_id=0
        )


def handle_command(event, vk, user_id, user_chats):
    """Handle slash commands"""
    command = event.text.lower().split()[0]

    if command == "/newchat":
        create_new_chat(user_id, user_chats)
        vk.messages.send(
            user_id=user_id,
            message="✅ Чат сброшен! Теперь вы начинаете новый диалог.",
            random_id=0
        )


def create_new_chat(user_id, user_chats):
    """Create new chat session and update storage"""
    try:
        chat_id = chai.create_chat().chat_id
        user_chats[user_id] = chat_id
        save_user_chats(user_chats)
        print(f"Created new chat for user {user_id} with chat_id {chat_id}")
    except Exception as e:
        print(f"Error creating new chat: {e}")
        raise


def main():
    """Main application entry point"""
    try:
        check_credentials()
        longpoll, vk = initialize_vk()
        user_chats = load_user_chats()

        print("Bot started successfully. Listening for messages...")

        while True:
            try:
                for event in longpoll.listen():
                    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                        handle_message(event, vk, user_chats)


            except vk_api.VkApiError as e:
                print(f"VK API error: {e}")
                # Wait before reconnecting
                time.sleep(10)
                continue
            except Exception as e:
                print(f"Unexpected error: {e}")
                # Wait before reconnecting
                time.sleep(10)
                continue

    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        print(f"Fatal error: {e}")
        print("Bot will now exit. Please check your configuration and try again.")


if __name__ == '__main__':
    import time

    main()