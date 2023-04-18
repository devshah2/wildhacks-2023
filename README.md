# TAi

## Command Line Arguments

Runs the server with a default transcript being read off automatically
```shell
python server.py
```

Runs the server using the voice-to-text feature to generatet the transcript
```shell
python server.py --voice
```

Runs the server using an arbitrary text file for the transcript
```shell
python server.py --transcript_file [FILENAME]
```

You can also add the flag `--key [KEY]` to change the default generated Professor access key

## Installation (MacOS)

Install portaudio:

```shell
brew install portaudio
```

Update pip and install requirements:

```shell
pip install --upgrade pip
pip install -r requirements.txt
```

Additionally, set the environment variable "OPENAI_API_KEY" to your OpenAI API Key which can be generated [Here](https://platform.openai.com/account/api-keys).

Run the app:
```shell
python3 server.py
```
