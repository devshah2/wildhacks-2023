import flask as fk
import uuid as pyuuid
import tai
from transcript import Transcript

app = fk.Flask(__name__)
app.config['SECRET_KEY'] = str(pyuuid.uuid4().hex)
app.config['SESSION_PERMANENT'] = False

# Kind of arbitrary but this is a safe number for testing
WINDOW_SIZE = 4096

unanswered_questions = []
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
    return fk.render_template("professor_view_bootstrap.html")

@app.route("/student")
def student():
    return fk.render_template("student_view_bootstrap.html")

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
    # Start threads here
    

    # 
    app.run(host='0.0.0.0',port=5000)


if __name__ == "__main__":
    main()

