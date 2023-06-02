"""Models for Blogly."""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(50), nullable=False)

    last_name = db.Column(db.String(50), nullable=False)

    image_url = db.Column(db.Text, nullable=True, default=None)

    def __repr__(self):
        """Change the default representation of the object"""

        user = self

        return f"<User id={user.id}, first_name={user.first_name}, last_name={user.last_name}, image_url={user.image_url}>"


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.Text, nullable=False)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", backref="posts")

    tags = db.relationship("PostTag", backref="posts")

    def __repr__(self):
        """Change the default representation of the object"""

        post = self

        return f"<Post id={post.id}, title={post.title}, content={post.content}, created_at={post.created_at}>"


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship("PostTag", backref="tags")

    def __repr__(self):
        """Change the default representation of the object"""

        tag = self

        return f"<Tag id={tag.id}, name={tag.name}>"


class PostTag(db.Model):
    __tablename__ = "post_tag"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)

    def __repr__(self):
        """Change the default representation of the object"""

        post_tag = self

        return f"<PostTag post_id={post_tag.post_id}, tag_id={post_tag.tag_id}>"
