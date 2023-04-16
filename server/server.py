import flask as fk
import uuid
import json
import jsonpickle as jsp
import markupsafe as mks

app = fk.Flask(__name__)
app.secret_key = "holyshitthisisunsafesomeonegeneratearealsecretkeybutimtoolazysonotme"

def generate_questions(transcript):
    return list(["How does that work?"])

@app.route("/", methods=["GET"])
def index():
    if not 'uuid' in fk.session:
        # Initialize the session
        init_session()
    return fk.redirect(fk.url_for('session'))

def init_session():
    fk.session['uuid'] = uuid.uuid4()
    fk.session['transcript'] = ''
    fk.session['transcript_changed'] = True
    fk.session['questions'] = []

    return fk.redirect(fk.url_for('session'))

@app.route("/session", methods=["GET"])
def session():
    if not 'uuid' in fk.session:
        return "<p>Session Not Found!</p>", 404
    uuid = fk.session['uuid']
    if fk.session['transcript_changed']:
        fk.session['questions'] = generate_questions(fk.session['transcript'])
        fk.session['transcript_changed'] = False
    questions: list[str] = fk.session['questions']
    return fk.render_template(
            'session_bootstrap.html', 
            questions=questions,
            uuid=uuid)

@app.route("/append_transcript", methods=["POST"])
def append_transcript():
    addition = fk.request.form['addition']
    if not 'transcript' in fk.session:
        fk.session['transcript'] = addition
    else:
        fk.session['transcript'] = fk.session['transcript'].join(addition)
    return fk.redirect(fk.url_for('session'))

@app.errorhandler(404)
def errorhandler_404(error):
    return fk.render_template("404.html"), 404

