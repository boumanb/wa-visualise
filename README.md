# wa-visualise

Python CLI tool that helps you visualise WhatsApp conversations.
- [x] Most common words
- [x] Most common messages
- [x] Message exchange frequency per day

## Installation

After creating and activating a new virtual environment.

```bash
git clone https://github.com/boumanb/wa-visualise.git
pip install -r requirements.txt

```


## Usage

Chat file has to be the original exported WhatsApp chat.
File containing the stop words has to be a ordinary .txt file with the stop words seperated by new lines

```bash
Usage: wa-visualise.py [OPTIONS] CHAT_FILE STOPWORDS_FILE

Options:
  --output_dir TEXT           Use this to set a certain output folder for the
                              charts. Default=output.
  --from_date TEXT            Use this to visualise from certain date.
                              [dd/mm/yy]
  --most_common_size INTEGER  Set the output size of the most common charts.
                              Default=50.
  --keep-emojis               Setting this will keep emojis in output.
  --help                      Show this message and exit.

```

## Example usage

```bash
python wa-visualise.py exported_chat.txt stop_words.txt --most_common_size 30 --from_date 11-03-19

Options:
  --output_dir TEXT           Use this to set a certain output folder for the
                              charts. Default=output.
  --from_date TEXT            Use this to visualise from certain date.
                              [dd/mm/yy]
  --most_common_size INTEGER  Set the output size of the most common charts.
                              Default=50.
  --keep-emojis               Setting this will keep emojis in output.
  --help                      Show this message and exit.

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
