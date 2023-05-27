"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User, Post
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
    """Redirect to list of users"""

    return redirect("/users")


@app.route("/users")
def display_users():
    """Display list of users from the DB"""

    users = User.query.all()

    return render_template("users.html", users=users)


@app.route("/users/<int:user_id>")
def show_user_details(user_id):
    """Display user details page"""

    user = User.query.get_or_404(user_id)

    return render_template("user_details.html", user=user)


@app.route("/users/new")
def create_user_form():
    """Display create user form page"""

    return render_template("create_user.html")


@app.route("/users/new", methods=["POST"])
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

    return redirect("/users")


@app.route("/users/<int:user_id>/edit")
def edit_user_form(user_id):
    """Display edit user form"""

    user = User.query.get_or_404(user_id)

    return render_template("edit_user.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def update_user(user_id):
    """Update an existing user"""

    user = User.query.get_or_404(user_id)
    image_url = request.form["image-url"]
    image_url = image_url if image_url else None

    user.first_name = request.form["first-name"]
    user.last_name = request.form["last-name"]
    user.image_url = image_url

    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/delete")
def delete_user(user_id):
    """Delete an existing user"""

    user = User.query.get_or_404(user_id)

    db.session.delete(user)

    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/posts/new")
def create_post_form(user_id):
    """Show form to create a post for a user"""

    user = User.query.get_or_404(user_id)

    return render_template("create_post.html", user=user)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def create_post(user_id):
    """Create a post for the user and save it to the DB"""

    user = User.query.get_or_404(user_id)

    title = request.form["title"]
    content = request.form["content"]

    new_post = Post(title=title, content=content, user_id=user.id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user.id}")


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Display a specific post"""

    post = Post.query.get_or_404(post_id)

    return render_template("post.html", post=post)
