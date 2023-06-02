"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User, Post, Tag, PostTag
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
    tags = []

    for tag in post.tags:
        tags.append(db.session.get(Tag, tag.tag_id))

    return render_template("post.html", post=post, tags=tags)


@app.route("/posts/<int:post_id>/edit")
def show_post_form(post_id):
    """Display form to edit a post"""

    post = Post.query.get_or_404(post_id)

    return render_template("edit_post.html", post=post)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def update_post(post_id):
    """Update a specific post"""

    post = Post.query.get_or_404(post_id)

    title = request.form["title"]
    content = request.form["content"]

    post.title = title
    post.content = content

    db.session.commit()

    return redirect(f"/users/{post.user_id}")


@app.route("/posts/<int:post_id>/delete")
def delete_post(post_id):
    """Delete a specific post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")


@app.route("/tags")
def display_tags():
    """Lists all tags, with links to the tag detail page"""

    tags = Tag.query.all()

    return render_template("tags.html", tags=tags)


@app.route("/tags/new")
def create_tag_form():
    """Shows a form to add a new tag"""

    return render_template("create_tag.html")


@app.route("/tags/new", methods=["POST"])
def create_tag():
    """Process add form, adds, tag and redirect to tag list"""

    name = request.form["name"]

    tag = Tag(name=name)

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")


@app.route("/tags/<int:tag_id>")
def tag_details(tag_id):
    """Show detail about a tag with links to edit form and to delete"""

    tag = Tag.query.get_or_404(tag_id)

    posts = []

    for post in tag.posts:
        posts.append(db.session.get(Post, post.post_id))

    return render_template("tag_details.html", tag=tag, posts=posts)


@app.route("/tags/<int:tag_id>/edit")
def edit_tag_form(tag_id):
    """Show edit form for a tag"""

    tag = Tag.query.get_or_404(tag_id)

    return render_template("edit_tag.html", tag=tag)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    """Process edit form, edit tag, and redirects to the tags list"""

    tag = Tag.query.get_or_404(tag_id)

    name = request.form["name"]

    tag.name = name

    db.session.commit()

    return redirect("/tags")
