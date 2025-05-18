# ChaiVkBot
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/MAKTPAXEP_MAKAHOB)

## Overview
A simple synchronous VK bot that connects to Character.ai, allowing users to chat with AI characters directly from VK Messenger.

## Features
+ Sending and recieving messages from vk to character.ai
+ Simple vk integration, including changing user status to "Typing", while waiting for character.ai response


## Installation & Setup
1. Clone the repo:
```
git clone https://github.com/true-sigma/ChaiVkBot.git && cd ChaiVkBot
```
2. Set up venv:
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
3. Insert credentials in /config/settings.py
   + [VK creds](https://vkhost.github.io/)
   + [Cai creds](https://github.com/kramcat/CharacterAI/blob/main/examples/sync/login.py)
5. Run main.py
