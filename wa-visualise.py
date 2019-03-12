import os
import string
import unicodedata
import click as click
import matplotlib.pyplot as plt
from matplotlib import rcParams
import logging

from classes.chat import Chat

valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
char_limit = 255

rcParams.update({'figure.autolayout': True})

logger = logging.getLogger()
logger.setLevel(logging.ERROR)


def load_txt_file(file_name):
    with open(file_name, encoding='utf-8') as f:
        return f.read().splitlines()


def clean_filename(filename, whitelist=valid_filename_chars, replace=' '):
    # replace spaces
    for r in replace:
        filename = filename.replace(r, '_')

    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()

    # keep only whitelisted chars
    cleaned_filename = ''.join(c for c in cleaned_filename if c in whitelist)
    if len(cleaned_filename) > char_limit:
        print(
            "Warning, filename truncated because it was over {}. Filenames may no longer be unique".format(char_limit))
    return cleaned_filename[:char_limit]


def plot_save_frequency(message_frequency_info, output_dir):
    plt.title('Amount of messages per day')
    for participant in message_frequency_info.keys():
        plt.plot(message_frequency_info.get(participant).keys(),
                 message_frequency_info.get(participant).values(),
                 label=participant)
    plt.legend()
    plt.gcf().autofmt_xdate()
    plt.savefig(output_dir + '/chat_message_frequency.png')


def plot_save_most_common(counter_data, title, most_common_size, output_dir):
    plt.figure(figsize=(8, 8))
    plt.gca().invert_yaxis()
    plt.title(str(most_common_size) + ' ' + title)
    plt.barh(*zip(*counter_data))
    plt.savefig(output_dir + '/' + clean_filename(title) + '.png')


@click.command()
@click.argument('chat_file', type=click.Path(exists=True))
@click.option('--stop_words', type=click.Path(exists=True), help='Use this to set the stop words file.')
@click.option('--output_dir', help='Use this to set a certain output folder for the charts. Default=output.',
              default='output')
@click.option('--from_date', help='Use this to visualise from certain date. [dd/mm/yy]')
@click.option('--most_common_size', type=int, help='Set the output size of the most common charts. Default=50.')
@click.option('--keep-emojis', is_flag=True, help='Setting this will keep emojis in output.')
def main(chat_file, stop_words, from_date, most_common_size, keep_emojis, output_dir):
    if not most_common_size:
        most_common_size = 50
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    if stop_words:
        stop_words = load_txt_file(stop_words)
    chat_contents = load_txt_file(chat_file)
    chat = Chat(chat_contents, stop_words, from_date=from_date, keep_emojis=keep_emojis)

    plot_save_frequency(chat.message_frequency_info, output_dir)

    most_common_words_per_participant = chat.get_most_common_words_per_participant(most_common_size)

    for participant in most_common_words_per_participant:
        plot_save_most_common(most_common_words_per_participant.get(participant),
                              'most common words by ' + participant,
                              most_common_size, output_dir)

    most_common_messages_per_participant = chat.get_most_common_messages_per_participant(most_common_size)

    for participant in most_common_messages_per_participant:
        plot_save_most_common(most_common_messages_per_participant.get(participant),
                              'most common messages by ' + participant,
                              most_common_size, output_dir)


if __name__ == '__main__':
    main()
