"""Blogly application."""

from flask import Flask, render_template
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
