"""Authentication user models."""
from flask import flash, redirect, url_for
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login_manager


# The user_loader decorator allows flask-login to load the current user
# and grab their id.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash("You must be logged in to view that page.")
    return redirect(url_for("auth.login"))

class User(UserMixin, db.Model):
    """User account model."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    created_on = db.Column(db.DateTime, index=False, nullable=False)

    def __init__(self, name, email, password, is_admin=False, created_on=None):
        """Initialize the user."""
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.is_admin = is_admin
        self.created_on = created_on

    def set_password(self, password):
        """Set password."""
        self.password_hash = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        """Check password."""
        return check_password_hash(self.password_hash, password)
