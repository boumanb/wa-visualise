from collections import Counter
from datetime import datetime
import logging

from classes.message import Message

MOST_COMMON_SIZE = 20


def process_chat(messages, from_date=False, keep_emojis=False):
    message_list = []

    for index, chat_line in enumerate(messages):
        try:
            date_time = Message.extract_datetime(chat_line)
            send_by = Message.extract_sender(chat_line)
            message = Message.extract_message(chat_line, keep_emojis)
        except ValueError as error:
            logging.error(error, exc_info=True)
        else:
            if from_date and date_time > datetime.strptime(from_date, '%d-%m-%y'):
                message = Message(chat_line, date_time, send_by, message)
                message_list.append(message)
            elif not from_date:
                message = Message(chat_line, date_time, send_by, message)
                message_list.append(message)
    return message_list


class Chat:
    message_amount_info = {}
    word_amount_info = {}
    message_frequency_info = {}
    participants = []

    def __init__(self, messages, stop_words=False, from_date=False, keep_emojis=False):
        self.messages = process_chat(messages, from_date, keep_emojis)
        self.stop_words = stop_words
        self.load_participants()
        self.load_message_amount_info()
        self.load_word_amount_info()
        self.load_message_daily_info()

    def load_message_amount_info(self):
        for name in self.participants:
            self.message_amount_info[name] = len([message.message for message in self.messages if
                                                  message.send_by == name])

    def load_word_amount_info(self):
        for name in self.participants:
            word_count = 0
            messages = [message.message for message in self.messages if
                        message.send_by == name]
            for message in messages:
                for word in message.split(' '):
                    if word and self.stop_words and word not in self.stop_words:
                        word_count += 1
                    elif word and not self.stop_words:
                        word_count += 1
            self.word_amount_info[name] = word_count

    def load_message_daily_info(self):
        for name in self.participants:
            self.message_frequency_info[name] = Counter(
                [message.dt_stamp.date() for message in self.messages if message.send_by == name])

    def load_participants(self):
        for message in self.messages:
            if message.send_by not in self.participants:
                self.participants.append(message.send_by)

    def get_most_common_words_per_participant(self, most_common_words_size=MOST_COMMON_SIZE):
        most_common_words_per_participant = {}
        for participant in self.participants:
            words = []
            messages = [message.message for message in self.messages if message.send_by == participant]
            for sentence in messages:
                for word in sentence.split(' '):
                    if word and self.stop_words and word not in self.stop_words:
                        words.append(word)
                    elif word and not self.stop_words:
                        words.append(word)
            most_common_words_per_participant[participant] = words

        for participant in most_common_words_per_participant.keys():
            most_common_words_per_participant[participant] = Counter(
                most_common_words_per_participant.get(participant)).most_common(most_common_words_size)

        return most_common_words_per_participant

    def get_most_common_messages_per_participant(self, most_common_messages_size=MOST_COMMON_SIZE):
        most_common_messages_per_participant = {}
        for participant in self.participants:
            if self.stop_words:
                most_common_messages_per_participant[participant] = Counter(
                    [message.message for message in self.messages
                     if message.send_by == participant
                     and message.message not in self.stop_words
                     and message.message is not '']).most_common(
                    most_common_messages_size)
            else:
                most_common_messages_per_participant[participant] = Counter(
                    [message.message for message in self.messages
                     if message.send_by == participant
                     and message.message is not '']).most_common(
                    most_common_messages_size)

        return most_common_messages_per_participant
