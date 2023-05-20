"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://postgres:{os.environ.get('DB_PASSWORD')}@localhost/blogly"
app.config["SQLALCHEMY_ECHO"] = True

connect_db(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home_page():
    """Display home page"""

    users = User.query.all()

    return render_template("home.html", users=users)


@app.route("/users/create")
def create_user_form():
    """Display create user form page"""

    return render_template("create_user.html")


@app.route("/users", methods=["POST"])
def create_user():
    """Create and add a new user to the Users DB"""

    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["image-url"]
    image_url = image_url if image_url else None

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    with app.app_context():
        db.session.add(new_user)
        db.session.commit()
        db.session.refresh(new_user)

    return redirect(f"/users/{new_user.id}")
