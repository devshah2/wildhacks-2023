import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_prompt(transcript):
  return """TAi is a college student who is watching a class 
  and has some questions about the content being taught.
  The following text within () is the transcript of the lecture so far: ({})
  What are some questions that TAi might have?""".format(transcript)

def get_questions(prof_tscpt):
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=generate_prompt(prof_tscpt),
    temperature=0.5,
    )
  return [choice.text for choice in response.choices]
