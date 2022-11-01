import requests

from settings import CHANNELS, BOT_TOKEN


def botq(method, params=None):
    api = f'https://api.telegram.org/bot%s/' % BOT_TOKEN

    url = api + method
    params = params or {}

    return requests.post(url, params).json()


def send_to_all(msg):
    for c in CHANNELS:
        reply(c, msg)


def reply(to, msg):
    if type(to) not in [int, str]:
        to = get_to_from_msg(to)
    resp = botq('sendMessage',
                {'chat_id': to, 'text': msg, 'disable_web_page_preview': True, 'parse_mode': 'Markdown'})
    return resp


def get_to_from_msg(msg):
    try:
        to = msg['chat']['id']
    except:
        to = ''

    return to
