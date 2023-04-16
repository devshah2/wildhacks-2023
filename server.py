import flask as fk
import uuid as pyuuid
import tai
from transcript import Transcript
from question import Question
import speech_to_text as spt
import threading

from transcript_to_stream import send_transcript_thread

app = fk.Flask(__name__)
app.config['SECRET_KEY'] = str(pyuuid.uuid4().hex)
app.config['SESSION_PERMANENT'] = False

# Kind of arbitrary but this is a safe number for testing
WINDOW_SIZE = 4096
transcript = Transcript(WINDOW_SIZE)
questions: list[Question] = []
prof_access_key = 'abcd'

def generate_questions(transcript):
    return list(tai.get_questions(transcript))

@app.route("/", methods=["GET"])
def index():
    print(fk.session)
    if 'prof' in fk.session and fk.session['prof']:
        return fk.redirect(fk.url_for("professor"))
    else:
        return fk.redirect(fk.url_for("student"))


@app.route("/access_key", methods=["POST"])
def access_key():
    print("Access key called")
    access_key = str(fk.request.form['access_key'])
    if access_key == prof_access_key:
        fk.session['prof'] = True
        return fk.redirect(fk.url_for('professor'))
    else:
        fk.abort(403)

@app.route("/professor")
def professor():
    if not 'prof' in fk.session:
        fk.abort(403)
    return fk.render_template("professor_view_bootstrap.html",
                              transcript=transcript.get_full(),
                              questions=questions)

@app.route("/student", methods=["GET"])
def student():
    return fk.render_template("student_view.html",
                              transcript=transcript.get_full(),
                              questions=questions)

@app.route("/student", methods=["POST"])
def student_post_question():
    question = fk.request.form['question']
    questions.append(Question(question))
    return fk.redirect(fk.url_for("student"))

@app.errorhandler(500)
def errorhandler_500(error):
    return fk.render_template("500.html"), 500

@app.errorhandler(404)
def errorhandler_404(error):
    return fk.render_template("404.html"), 404

@app.errorhandler(403)
def errorhandler_403(error):
    return fk.render_template("403.html"), 403

def main():

    shutdown = threading.Event()
    shutdown.clear()

    # Start threads here
    speech_to_text_enabled = False
    if speech_to_text_enabled:
        spt_thread = threading.Thread(target=spt.speech_recog_thread, args=[transcript, shutdown])
        spt_thread.start()
    else:
        st_thread = threading.Thread(target=send_transcript_thread, args=[transcript, shutdown])
        st_thread.start()

    # 
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

