import time

import requests

from config.settings import BOT_TOKEN

URL = f'https://api.telegram.org/bot{BOT_TOKEN}'


def get_updates(offset=None):
    url = URL + '/getUpdates'
    params = {'timeout': 100, 'offset': offset}
    response = requests.get(url, params=params)
    result_json = response.json()['result']
    return result_json


def send_message(chat_id, text):
    url = URL + '/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, data=payload)


def handle_updates(updates):
    for update in updates:
        message = update.get('message')
        if not message:
            continue

        chat_id = message['chat']['id']
        text = message.get('text')

        if text == '/start':
            send_message(chat_id, 'Hi! Welcome to your habit tracker bot.')


def main():
    offset = None
    while True:
        updates = get_updates(offset)
        if updates:
            handle_updates(updates)
            offset = updates[-1]['update_id'] + 1
        time.sleep(1)


if __name__ == '__main__':
    main()
