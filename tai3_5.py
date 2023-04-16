import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_personality(class_level):
  return f"""You are a class assistant for a {class_level} level 
    class. Given a transcript from 
    the professor speech, come up with a relevant question about 
    the content being taught. If there is no relevant question 
    can be asked, say '0' and nothing else."""

def get_questions(class_lvl, prof_tscpt):
  
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages = [
      {"role": "system", "content": generate_personality(class_lvl)},
      {"role": "user", "content": prof_tscpt}
      ],
    temperature=0.5,
    top_p=0
    )
  question = response.choices[0].message.content
  if question[0] == "0":
    return ""
  else:
    return question
