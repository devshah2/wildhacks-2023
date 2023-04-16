import os
import sys
from string import ascii_lowercase
import random
import flask as fk
import flask_sock as fks
import uuid as pyuuid
from transcript import Transcript
from question import Question
import speech_to_text as spt
import threading
from generate_question import update_questions
from answer_questions_updater import answer_questions
from filter_questions import erase_questions
from gptconfig import Gptconfig
from transcript_to_stream import send_transcript_thread
import argparse

app = fk.Flask(__name__)
app.config['SECRET_KEY'] = str(pyuuid.uuid4().hex)
app.config['SESSION_PERMANENT'] = False

sock = fks.Sock(app)

# Kind of arbitrary but this is a safe number for testing
WINDOW_SIZE = 4096
transcript = Transcript(WINDOW_SIZE)
questions: dict[pyuuid.UUID, Question] = {}
config = Gptconfig("0.5", "undergraduate", 30)
prof_access_key = ''.join(random.sample(ascii_lowercase,4))

class SessionInfo:

    def __init__(self, uuid):
        self.uuid = uuid
        self.is_prof = False
        self.upvoted_questions = set()

    def set_prof(self):
        self.is_prof = True

sinfo: dict[pyuuid.UUID, SessionInfo] = {}

@app.route("/", methods=["GET"])
def index():
    print(fk.session)
    if not 'uuid' in fk.session:
        uuid = pyuuid.uuid4()
        fk.session['uuid'] = uuid
        sinfo[uuid] = SessionInfo(uuid)
    else:
        uuid = fk.session['uuid']

    if sinfo[uuid].is_prof:
        return fk.redirect(fk.url_for("professor"))
    else:
        return fk.redirect(fk.url_for("student"))


@app.route("/access_key", methods=["POST"])
def access_key():
    print("Access key called")
    access_key = str(fk.request.form['access_key'])
    if access_key == prof_access_key:
        sinfo[fk.session['uuid']].is_prof = True
        return fk.redirect(fk.url_for('professor'))
    else:
        fk.abort(403)

@app.route("/upvote/<question_uuid>", methods=["POST"])
def upvote(question_uuid):
    quuid = pyuuid.UUID(question_uuid)
    if not quuid in questions.keys():
        fk.abort(404)
    question = questions[quuid]
    if question in sinfo[fk.session['uuid']].upvoted_questions:
        question.votes_decrement()
        sinfo[fk.session['uuid']].upvoted_questions.remove(question)
    else:
        question.votes_increment()
        sinfo[fk.session['uuid']].upvoted_questions.add(question)

    return fk.redirect(fk.url_for("student"))

@app.route("/professor", methods=["GET"])
def professor():
    if not sinfo[fk.session['uuid']].is_prof:
        fk.abort(403)
    all_questions = list(questions.values())
    all_questions.sort(key=lambda q: q.get_votes(), reverse=True)
    return fk.render_template("professor_view_bootstrap.html",
                              transcript=transcript.get_full(),
                              questions=all_questions,
                              constant_refresh=True,
                              websockets=False,
                              class_lvl=config.get_class_lvl(),
                              creativity=config.get_temperature(),
                              generation=config.get_generation_speed(),
                              sort="Upvotes")

@app.route("/professor", methods=["POST"])
def professor_post_update():
    data = fk.request.get_json()
    # Access the selected values from the dropdowns in the data object
    config.set_class_lvl(data.get('class')) 
    config.set_temperature(data.get('creativity')) 
    config.set_generation_speed(data.get('generation'))
    sorting_option = data.get('sort')
    print(data.get('generation'))
    print(data)
    print(config.get_class_lvl())
    return fk.redirect(fk.url_for("professor"))

@app.route("/student", methods=["GET"])
def student():
    return fk.render_template("student_view.html",
                              transcript=transcript.get_full(),
                              questions=questions,
                              constant_refresh=False,
                              websockets=True,
                              is_prof=sinfo[fk.session['uuid']].is_prof)

@app.route("/student", methods=["POST"])
def student_post_question():
    question = fk.request.form['question']
    quuid = pyuuid.uuid4()
    questions[quuid] = Question(quuid, question, votes=0, is_student=True, author="Student")
    return fk.redirect(fk.url_for("student"))

@sock.route("/transcript")
def send_transcript(sock):
    while not shutdown.is_set():
        data = sock.receive()
        sock.send(transcript.get_full())
@sock.route("/questions")
def send_questions(sock):
    while not shutdown.is_set():
        data = sock.receive()
        student_questions_card = fk.render_template("student_view_questions.html",
                                                    transcript=transcript.get_full(),
                                                    questions=questions,
                                                    constant_refresh=False,
                                                    websockets=True)
        sock.send(student_questions_card)

@app.errorhandler(500)
def errorhandler_500(error):
    return fk.render_template("500.html"), 500

@app.errorhandler(404)
def errorhandler_404(error):
    return fk.render_template("404.html"), 404

@app.errorhandler(403)
def errorhandler_403(error):
    return fk.render_template("403.html"), 403

shutdown = threading.Event()
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--voice', action=argparse.BooleanOptionalAction)
    parser.add_argument('--transcript_file', default="example_lecture.txt")
    parser.add_argument('--addr', default="0.0.0.0")

    args = parser.parse_args()

    shutdown.clear()

    # Start threads here
    speech_to_text_enabled = bool(args.voice)
    if speech_to_text_enabled:
        print("Speech to text enabled!")
        spt_thread = threading.Thread(target=spt.speech_recog_thread, args=[transcript, shutdown])
        spt_thread.start()
    else:
        print("Transcript File: ", args.transcript_file)
        st_thread = threading.Thread(target=send_transcript_thread, args=[transcript, shutdown, args.transcript_file])
        st_thread.start()

    gen_thread = threading.Thread(target=update_questions, args=[transcript, shutdown, questions, config])
    gen_thread.start()

    erase_thread = threading.Thread(target=erase_questions, args=[questions, shutdown, 5])
    erase_thread.start()    

    ans_thread = threading.Thread(target=answer_questions, args=[transcript, shutdown, questions, 0.1, 15])
    ans_thread.start()
    # 
    print("")
    print("Server Starting: Professor Access Key Is: ", prof_access_key)
    print("")
    app.run(host='0.0.0.0',port=5000)

    print("Shutting down...")
    shutdown.set()

    if speech_to_text_enabled:
        print("joining spt_thread")
        spt_thread.join()
        print("spt_thread joined!")
    else:
        print("joining st_thread")
        st_thread.join()
        print("st_thread joined!")


if __name__ == "__main__":
    main()
