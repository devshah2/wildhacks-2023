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

## Project Information
### Inspiration
As students, we often hesitate to ask questions because we believe they may not be significant enough or can be addressed later. However, we fail to recognize that these questions may be common among our peers. That's why having an assistant that generates questions and allows students to submit written inputs could prove to be incredibly beneficial.

### What it does
TAi is an innovative AI assistant that revolutionizes the way we ask and answer questions in the classroom. By actively listening to the lecture, TAi generates relevant questions, gauging the appropriateness of the timing. It also provides a platform for students to submit their own written questions, which are ranked using an upvoting system. As the lecture progresses, TAi searches for answers to the current questions on the live transcript and moves them to the "Answered" section with appropriate citations. Additionally, students have access to the live transcript, making it easier to follow along with the lecture.

### How we built it
The AI assistant was built using three key components. GPT-3 was used to generate new questions using carefully created prompts. This prompt was modifiable based on the professor's live inputs. A BERT model fine tuned on SQUAD data was used for finding answers to questions from the transcript. This model was used from the huggingface API and was run on all unanswered questions periodically providing information about the new content said. Lastly, the de-duplication of questions was done by finding the cosine similarity between questions. To do so, an embedding was trained using a transformer and each question's embedding was compared to others prioritizing answered questions as well as students questions. The front end used HTML and Bootstrap CSS framework. The back end used a Flask python server running on the "Professor's" machine, so that the python speech_recognition library could be used alongside the server instance for UI if that was desired. The website itself uses Flask secure sessions to keep the professors view separate from that of the students. And it is able to be live updated using websockets to avoid reloading. The data is never moved to persistent storage allowing for privacy to be maintained. Lastly, the flask web app is set up such that given the correct link students on the same network can directly join.

### Challenges we ran into
The initial prompt given to GPT-3 defines how the assistant is gonna behave, so we had to do many iterations to find the model's set of parameters that fits our needs the best. Additionally, efficiently running the pipeline without causing screen freezes or unecessary delays became a growing concern. We tackled this using multithreading as well as discrete functions and classes for specific tasks. Tuning the thresholds and some key parameters was also a challenge that we had to solve using educated trial and error.

### Accomplishments that we're proud of
It is actually satisfying to see the audio being transformed to transcript, the assistant generating and matching questions to answers, and the upvoting system working, everything live. It was truly remarkable to see how the answering model would try and answer each of the GPT-3 questions in real time as well as the student questions whilst the de-duplication model kept all questions in check. Seeing the quality of the answers whilst having multiple student devices connected to the professor was a truly great achievement.

### What we learned
Giving less 'training' (example question-answer phrases) to GPT-3 can be better. There are many AI models other than GPT-3 that do their jobs really well and this was a hypothesis we proved right by using specialized models for tasks. This meant that we used SotA frameworks and gained the best possible reuslts. All of us gained a large amount of skills in terms of API usage, LLM training and inference, server-side development using flask, and lastly networking.

### What's next
Now that we have a working system for generating questions and presenting them to the professor in a ranked manner, we would like to add a feature for the professor to either accept or reject the citation provided by the AI. Then, they can either discard the question or display the citation to the students. The current implementation of the speech-to-text feature uses a very basic Python library as a proof of concept, which is highly error-prone. Therefore, we plan to interface with a better transcription system in the future, possibly even utilizing the Panopto API directly to obtain a high-quality live transcript of the lectures.
