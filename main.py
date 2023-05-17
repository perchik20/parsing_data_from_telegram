from telethon import TelegramClient
import time
from config import api_id, api_hash

client = TelegramClient('anon', api_id, api_hash) # announcing a client to work with telegram
msg = {} # announcing dict for message


class ParserTelegram:

    """Class which responsible for get info from
    telegram groups or public, there are two function
    1. get info from few groups
    2. gey message with key words"""

    def __init__(self, api_id, api_hash):
        self.api_id = api_id
        self.api_hash = api_hash

    async def get_message(self, name):

        counter = 0
        # catch only last message from public
        async for message in client.iter_messages(f'{name}'):
            # memorizing the id
            channel_id = message.peer_id.channel_id
            date = str(message.date)

            if counter > 0:
                break

            try:
                # check message in dikt msg
                if msg[str(channel_id)] != str(date):
                    await client.forward_messages('me', message)
                    msg.update({f'{channel_id}': f'{date}'})
            except:
                # first add in dikt msg
                await client.forward_messages('me', message)
                msg.update({f'{channel_id}': f'{date}'})
            finally:
                # add one to global counter
                counter += 1

    async def search_with_key_word(self, username, keyword):

        counter = 0
        async for message in client.iter_messages(f'{username}'):
            channel_id = message.peer_id.channel_id
            date = str(message.date)

            if counter > 0:
                break

            try:
                if msg[str(channel_id)] != str(date) and keyword in message.text:
                    await client.forward_messages('me', message)
                    msg.update({f'{channel_id}': f'{date}'})
            except:
                if keyword in message.text:
                    await client.forward_messages('me', message)
                    msg.update({f'{channel_id}': f'{date}'})
            finally:
                counter += 1


def methods(Parser, point):
    if point == '1':
        channels = input('Введите ники каналов через пробел без знака "@": ').split()
        while True:
            with client:
                for name in channels:
                    client.loop.run_until_complete(Parser.get_message(name))
                time.sleep(1)
    elif point == '2':
        channels = input('Введите ники каналов через пробел без знака "@": ').split()
        keyword = input('Введите ключевое слово: ')
        while True:
            with client:
                for i in channels:
                    client.loop.run_until_complete(Parser.search_with_key_word(i, keyword))
                time.sleep(1)


if __name__ == '__main__':
    Parser = ParserTelegram(api_id, api_hash)
    point = input('Выбор: ')
    methods(Parser, point)

