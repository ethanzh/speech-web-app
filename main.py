from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    abort,
    send_file,
    jsonify,
)
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)
import sqlite3
import bcrypt
import os


from peewee import DoesNotExist
from pathlib import Path
from helpers import (
    init_db,
    init_dirs,
    get_all_text_details,
    get_text_detail,
    format_email,
    flash_errors,
    delete_sample,
)
from forms import LoginForm, CreateAccountForm
from models import User, UserSample
from config import Config
import uuid

app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager()
login_manager.init_app(app)

init_db()
init_dirs()

DATA_DIR = "data"


@login_manager.user_loader
def user_loader(user_id):
    try:
        return User.get(User.id == user_id)
    except DoesNotExist:
        return None


@app.route("/")
def home():
    if not (current_user and current_user.is_authenticated):
        return redirect(url_for("login"))

    user_samples = [ur.filename for ur in current_user.samples]
    return render_template(
        "home.html",
        user_samples=user_samples,
        text_details=get_all_text_details(),
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if not form.validate_on_submit():
        return render_template("login.html", form=form)

    try:
        user = User.get(User.email == format_email(form.email.data))
    except DoesNotExist:
        flash("This email and password combination doesn't exist")
        return redirect(url_for("create_account"))

    if not bcrypt.checkpw(
        form.password.data.encode("utf-8"), user.salted_pw.encode("utf-8")
    ):
        flash("This email and password combination doesn't exist")
        return redirect(url_for("create_account"))

    login_user(user)
    return redirect(url_for("home"))


@app.route("/create_account", methods=["GET", "POST"])
def create_account():
    form = CreateAccountForm()
    if form.validate_on_submit():
        formatted_email = format_email(form.email.data)
        hashed_salted_pw = bcrypt.hashpw(
            form.password.data.encode("utf-8"), bcrypt.gensalt()
        )

        if User.select().where(User.email == formatted_email).count() > 0:
            flash(f"Account with email {formatted_email} already exists")
            return redirect(url_for("login"))

        new_user = User.create(
            id=uuid.uuid4(),
            email=formatted_email,
            salted_pw=hashed_salted_pw,
            gender=form.gender.data,
            age_range=form.age_range.data,
            language=form.language.data,
        )

        login_user(new_user)

        return redirect(url_for("home"))
    else:
        flash_errors(form)

    return render_template("create_account.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/blank", methods=["GET"])
@login_required
def text_blank():
    samples = []
    for sample in current_user.samples:
        if ".webm" not in sample.filename:
            continue

        samples.append({"id": sample.id, "created_at": sample.created_at})
    samples.reverse()
    return render_template("blank_text.html", samples=samples)


@app.route("/text/<string:text>", methods=["GET"])
@login_required
def text_detail(text):
    if text not in [t.name for t in get_all_text_details()]:
        return redirect(url_for("home"))

    text_detail = get_text_detail(text)
    status = text in [ur.filename for ur in current_user.samples]

    return render_template("text.html", text_detail=text_detail, status=status)


@app.route("/sample", methods=["POST"])
@login_required
def post_sample():
    data = request.files.to_dict().get("data")
    text = request.form.get("text")
    audio_source = request.form.get("audio_source")
    video_source = request.form.get("video_source")
    if not data:
        return jsonify(success=False)

    Path(f"{DATA_DIR}/{current_user.id}").mkdir(parents=True, exist_ok=True)
    if text:
        text_name = text.split(".")[0]
        num_samples_for_text = len(
            [s for s in current_user.samples if text_name in s.filename]
        )
        filename = f"{text_name}_{num_samples_for_text + 1}.wav"
        path = f"{DATA_DIR}/{current_user.id}/{filename}"
    else:
        files = os.listdir(f"{DATA_DIR}/{current_user.id}")
        num_blanks = len([f for f in files if ".webm" in f])
        filename = f"{num_blanks + 1}.webm"
        path = f"{DATA_DIR}/{current_user.id}/{filename}"

    data.save(path)
    UserSample.create(
        user=current_user.id,
        filename=filename,
        audio_source=audio_source,
        video_source=video_source,
    )

    return jsonify(success=True)


@app.route("/sample/<int:sample_id>", methods=["GET", "DELETE"])
@login_required
def handle_sample(sample_id=None):
    if request.method == "GET":
        sample = UserSample.get(id=sample_id)
        path = f"data/{current_user.id}/{sample.filename}"
        return send_file(path, as_attachment=True)

    elif request.method == "DELETE":
        delete_sample(sample_id)
        return jsonify(success=True)


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True)
