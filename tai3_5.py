import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_personality():
  return """You are a class assistant. Given a transcript from 
    the professor speech, come up with a relevant question about 
    the content being taught. If there is no relevant question 
    can be asked, say '0' and nothing else."""

class question:
  def __init__(self, prof, tai):
    self.prof = prof
    self.tai = tai

def standard_question():
  return question(
    prof="""Initially, let us assume that a thermodynamically
    large system is in thermal contact with the environment,
    with a temperature T, and both the volume of the system and
    the number of constituent particles are fixed.""",
    tai="What is a thermodynamically large system?")

def no_question():
  return question(
      prof="""Partition functions are functions of the
      thermodynamic state variables, such as the temperature
      and volume.""", 
      tai="")


def generate_prompt(transcript):
  return """TAi is a college student who is watching a class 
  and have some questions about the content being taught.
  Professor: Initially, let us assume that a thermodynamically
  large system is in thermal contact with the environment,
  with a temperature T, and both the volume of the system and
  the number of constituent particles are fixed.
  TAi: What is a thermodynamically large system?
  Professor: {}
  TAi:""".format(transcript)

def get_questions(prof_tscpt):
  
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages = [
      {"role": "system", "content": generate_personality()},
      {"role": "user", "content": prof_tscpt}
      ],
    temperature=0.5,
    top_p=0
    )
  return response.choices[0].message.content

if __name__ == "__main__":
  prof_t = """French is an awesome language. If you’re traveling 
  to France, you’ll know first hand."""
  student_q = get_questions(prof_t)
  if student_q[0] == "0":
    print("")
  else:
    print(student_q)
