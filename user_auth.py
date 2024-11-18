from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db, bcrypt, login_manager
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.exc import IntegrityError


# ---------------------
# User Model
# ---------------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)  # Add `unique=True`
    email = db.Column(db.String(120), unique=True, nullable=False)    # Add `unique=True`
    password_hash = db.Column(db.String(128), nullable=False)

    def to_dict(self):
        return {"id": self.id, "username": self.username, "email": self.email}


# Configure Flask-Login
login_manager.login_view = 'user_bp.login'  # Redirect to login if unauthenticated

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------------------
# Blueprint Setup
# ---------------------
user_bp = Blueprint('user_bp', __name__)

# ---------------------
# Routes
# ---------------------

@user_bp.route('/register', methods=['POST'])
def register():
    """
    Endpoint to register a new user.
    Expects JSON: {"username": "name", "email": "email", "password": "password"}
    """
    data = request.get_json()

    # Check if username or email already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already exists"}), 400

    # Hash the password and create a new user
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], email=data['email'], password_hash=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully", "user": new_user.to_dict()}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


@user_bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint to log in a user.
    Expects JSON: {"email": "email", "password": "password"}
    """
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password_hash, data['password']):
        login_user(user)
        return jsonify({"message": "Login successful", "user": user.to_dict()}), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401


@user_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    """
    Endpoint to log out the current user.
    """
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200


@user_bp.route('/protected', methods=['GET'])
@login_required
def protected():
    """
    A protected route that can only be accessed by logged-in users.
    """
    return jsonify({"message": f"Hello, {current_user.username}! You are logged in."})
