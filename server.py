import flask as fk
import uuid as pyuuid
import tai

app = fk.Flask(__name__)
app.secret_key = "holyshitthisisunsafesomeonegeneratearealsecretkeybutimtoolazysonotme"

class SessionData():

    def __init__(self, uuid):
        self.uuid = uuid
        self.transcript = ''
        self.transcript_changed = False
        self.questions = []

sdata: dict[pyuuid.UUID, SessionData] = {}

def generate_questions(transcript):
    return list(tai.get_questions(transcript))

@app.route("/", methods=["GET"])
def index():
    init_session()
    return fk.redirect(fk.url_for('session'))

def init_session():
    uuid = pyuuid.uuid4()
    fk.session['uuid'] = uuid
    sdata[uuid] = SessionData(uuid)
    return fk.redirect(fk.url_for('session'))

@app.route("/session", methods=["GET"])
def session():
    if not 'uuid' in fk.session:
        return "<p>Session Not Found!</p>", 404
    uuid = fk.session['uuid']
    if not uuid in sdata.keys():
        return "<p>Session Found but Session Data Not Found!</p>", 404
    if sdata[uuid].transcript_changed:
        sdata[uuid].questions = generate_questions(sdata[uuid].transcript)
        sdata[uuid].transcript_changed = False
    return fk.render_template(
            'session_bootstrap.html', 
            questions=sdata[uuid].questions,
            uuid=uuid)

@app.route("/append_transcript", methods=["POST"])
def append_transcript():
    uuid = fk.session['uuid']
    addition = fk.request.form['addition']
    sdata[uuid].transcript += addition
    sdata[uuid].transcript_changed = True
    print("Transcript Changed: ", sdata[uuid].transcript)
    return fk.redirect(fk.url_for('session'))

@app.errorhandler(500)
def errorhandler_500(error):
    return fk.render_template("500.html"), 500

@app.errorhandler(404)
def errorhandler_404(error):
    return fk.render_template("404.html"), 404

