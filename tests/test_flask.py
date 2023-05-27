from unittest import TestCase

from app import app
from models import db, User, Post
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Use test database and don't clutter tests with SQL
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://postgres:{os.environ.get('DB_PASSWORD')}@localhost/blogly_test"

app.config["TESTING"] = True

with app.app_context():
    db.drop_all()
    db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for users DB"""

    def setUp(self):
        """Add sample user"""

        user = User(first_name="Test", last_name="User")
        post = Post(title="Test Post", content="My test content")

        with app.app_context():
            Post.query.delete()
            User.query.delete()

            db.session.add(user)
            db.session.commit()

            # Refresh the user object to ensure it is still associated with an active session
            db.session.refresh(user)

            post.user_id = user.id

            db.session.add(post)
            db.session.commit()

            db.session.refresh(post)

        self.user_id = post.user_id
        self.post_id = post.id

    def tearDown(self):
        """Clean up any fouled transaction"""

        with app.app_context():
            db.session.rollback()

    def test_display_users(self):
        with app.test_client() as client:
            res = client.get("/users")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Test User", html)

    def test_show_user_details(self):
        with app.test_client() as client:
            res = client.get(f"/users/{self.user_id}")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Test User", html)
            self.assertIn("Edit", html)
            self.assertIn("Delete", html)

    def test_create_user_form(self):
        with app.test_client() as client:
            res = client.get("/users/new")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("<h1>Create a user</h1>", html)

    def test_create_user(self):
        with app.test_client() as client:
            data = {"first-name": "Test", "last-name": "User 2", "image-url": ""}
            res = client.post("/users/new", data=data, follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Test User 2", html)

    def test_create_post_form(self):
        with app.test_client() as client:
            res = client.get(f"/users/{self.user_id}/posts/new")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("<h1>Add Post for Test User</h1>", html)

    def test_create_post(self):
        with app.test_client() as client:
            data = {"title": "Test Post 2", "content": "Test content 2"}
            res = client.post(
                f"/users/{self.user_id}/posts/new", data=data, follow_redirects=True
            )
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Test Post 2", html)

    def test_show_post(self):
        with app.test_client() as client:
            res = client.get(f"/posts/{self.post_id}")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Test Post", html)

    def test_delete_post(self):
        with app.test_client() as client:
            res = client.get(f"/posts/{self.post_id}/delete")

            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, f"/users/{self.user_id}")

            with app.app_context():
                post = Post.query.get(self.post_id)
                self.assertIsNone(post)
