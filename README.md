# ChaiVkBot

A simple VK bot that connects to Character.ai, allowing users to chat with AI characters directly from VK Messenger.

### IMPORTANT NOTE
since vk_api has some weird bug in its code (as of may 2025), you'll need to change a few lines in /vk_api/longpoll.py:

#### From:
```
    def update_longpoll_server(self, update_ts=True):
        values = {
            'lp_version': '3',
            'need_pts': self.pts
        }
```
#### To:
```
    def update_longpoll_server(self, update_ts=True):
        values = {
            'lp_version': '3',
            'need_pts': '1'
        }
```
