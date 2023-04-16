import flask as fk
import uuid as pyuuid
import tai
from transcript import Transcript

app = fk.Flask(__name__)
app.secret_key = "holyshitthisisunsafesomeonegeneratearealsecretkeybutimtoolazysonotme"

# Kind of arbitrary but this is a safe number for testing
WINDOW_SIZE = 4096

unanswered_questions = []
prof_access_key = 'abcd'

def generate_questions(transcript):
    return list(tai.get_questions(transcript))

@app.route("/", methods=["GET"])
def index():
    if 'prof' in fk.session:
        return fk.redirect(fk.url_for("professor"))
    else:
        return fk.redirect(fk.url_for("student"))


@app.route("/access_key", methods=["POST"])
def access_key():
    access_key = str(fk.request.form['access_key'])
    if access_key == prof_access_key:
        fk.session['prof'] = True
        return fk.redirect(fk.url_for('professor'))
    else:
        return fk.redirect(fk.url_for('its_just_a_prank_bro'))

@app.route("/professor")
def professor():
    return fk.render_template("professor_view_bootstrap.html")

@app.route("/student")
def student():
    return fk.render_template("student_view_bootstrap.html")

@app.route("/its_just_a_prank_bro", methods=["GET"])
def its_just_a_prank_bro():
    return fk.render_template("scary_page.html")

@app.errorhandler(500)
def errorhandler_500(error):
    return fk.render_template("500.html"), 500

@app.errorhandler(404)
def errorhandler_404(error):
    return fk.render_template("404.html"), 404

def main():
    # Start threads here

    # 
    app.run()


if __name__ == "__main__":
    main()

