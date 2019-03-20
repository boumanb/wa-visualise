import re
from datetime import datetime

RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)


class Message:

    def __init__(self, raw, dt_stamp, send_by, message):
        self.raw = raw
        self.dt_stamp = dt_stamp
        self.send_by = send_by
        self.message = message


def extract_datetime(chat_line):
    date_time_str = chat_line.split('-')[0].replace(',', '').strip()
    date_time = datetime.strptime(date_time_str, "%m/%d/%y %H:%M")
    return date_time


def extract_message(chat_line, keep_emojis=False):
    if keep_emojis:
        message = chat_line.split(':')[2].strip().lower()
    else:
        message = RE_EMOJI.sub(r'', chat_line.split(':')[2].strip().lower())
    return message


def extract_sender(chat_line):
    return chat_line.split('-')[1].split(':')[0].strip()
