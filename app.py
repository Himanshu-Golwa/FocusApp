
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import login_required, current_user
from datetime import datetime
from extensions import db, bcrypt, login_manager
from user_auth import user_bp  # User authentication blueprint

# Initialize Flask app
app = Flask(__name__)
api = Api(app)
CORS(app)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'  # Required for Flask-Login

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)


# Initialize the database
db = SQLAlchemy(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)
# Register blueprints
app.register_blueprint(user_bp, url_prefix='/auth')

# ---------------------
# Database Models
# ---------------------
# Database model for tasks
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    timer_status = db.Column(db.String(20), default="stopped")  # running, paused, stopped
    elapsed_time = db.Column(db.Integer, default=0)  # Time in seconds
    start_time = db.Column(db.DateTime, nullable=True)  # Time when the timer started
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = relationship("User", backref="tasks")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "timer_status": self.timer_status,
            "elapsed_time": self.elapsed_time,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "user_id": self.user_id
        }

# ---------------------
# Task Management Routes
# ---------------------
class TaskList(Resource):
    @login_required
    def get(self):
        # Retrieve all tasks for the logged-in user
        tasks = Task.query.filter_by(user_id=current_user.id).all()
        return {"tasks": [task.to_dict() for task in tasks]}, 200

    @login_required
    def post(self):
        # Add a new task for the logged-in user
        data = request.get_json()
        if not data.get('title'):
            return {"error": "Task title is required"}, 400

        new_task = Task(
            title=data['title'],
            description=data.get('description', ""),
            user_id=current_user.id
        )
        try:
            db.session.add(new_task)
            db.session.commit()
            return {"message": "Task added successfully", "task": new_task.to_dict()}, 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500
        finally:
            db.session.close()


class StartTimer(Resource):
    @login_required
    def post(self):
        # Start timer logic for a specific task
            "start_time": self.start_time.isoformat() if self.start_time else None
        }

@app.route('/')
def home():
    return {"message": "Welcome to my Focus App API!"}

# Resource for handling tasks
class TaskList(Resource):
    def get(self):
        # Retrieve all tasks from the database
        tasks = Task.query.all()
        return {"tasks": [task.to_dict() for task in tasks]}

    def post(self):
        # Add a new task to the database
        data = request.get_json()
        new_task = Task(title=data['title'], description=data.get('description', ""))
        db.session.add(new_task)
        db.session.commit()
        return {"message": "Task added successfully", "task": new_task.to_dict()}, 201

class StartTimer(Resource):
    def post(self):
        # Start timer logic
        data = request.get_json()
        task_id = data.get("task_id")
        work_duration = data.get("work_duration", 25 * 60)  # Default: 25 minutes
        task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
        if not task:
            return {"error": "Task not found or you don't have access to it"}, 404
        task = Task.query.get(task_id)
        if not task:
            return {"error": "Task not found"}, 404

        # Start the timer
        task.timer_status = "running"
        task.start_time = datetime.utcnow()  # Set start time to now
        db.session.commit()

        return {"message": f"Timer started for task {task_id} for {work_duration // 60} minutes", "task": task.to_dict()}, 200

    @login_required
    def put(self):
        # Manage timer state: pause, resume, stop
        data = request.get_json()
        task_id = data.get("task_id")
        action = data.get("action")  # "pause", "resume", "stop"

        task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
        if not task:
            return {"error": "Task not found or you don't have access to it"}, 404

        try:
            if action == "pause":
                if task.timer_status != "running":
                    return {"error": "Timer is not running, cannot pause"}, 400

                # Calculate elapsed time and update
                elapsed = (datetime.utcnow() - task.start_time).total_seconds()
                task.elapsed_time += int(elapsed)
                task.timer_status = "paused"
                task.start_time = None

            elif action == "resume":
                if task.timer_status != "paused":
                    return {"error": "Timer is not paused, cannot resume"}, 400

                task.timer_status = "running"
                task.start_time = datetime.utcnow()

            elif action == "stop":
                if task.timer_status == "running":
                    # Calculate final elapsed time
                    elapsed = (datetime.utcnow() - task.start_time).total_seconds()
                    task.elapsed_time += int(elapsed)

                task.timer_status = "stopped"
                task.elapsed_time = 0
                task.start_time = None

            else:
                return {"error": "Invalid action"}, 400

            db.session.commit()
            return {"message": f"Timer {action}d for task {task_id}", "task": task.to_dict()}, 200
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500
        finally:
            db.session.close()
        task = Task.query.get(task_id)
        if not task:
            return {"error": "Task not found"}, 404

        if action == "pause":
            if task.timer_status != "running":
                return {"error": "Timer is not running, cannot pause"}, 400

            # Calculate elapsed time and update
            elapsed = (datetime.utcnow() - task.start_time).total_seconds()
            task.elapsed_time += int(elapsed)
            task.timer_status = "paused"
            task.start_time = None  # Clear start time

        elif action == "resume":
            if task.timer_status != "paused":
                return {"error": "Timer is not paused, cannot resume"}, 400

            task.timer_status = "running"
            task.start_time = datetime.utcnow()  # Reset start time

        elif action == "stop":
            if task.timer_status == "running":
                # Calculate final elapsed time
                elapsed = (datetime.utcnow() - task.start_time).total_seconds()
                task.elapsed_time += int(elapsed)

            task.timer_status = "stopped"
            task.elapsed_time = 0  # Reset elapsed time
            task.start_time = None  # Clear start time

        else:
            return {"error": "Invalid action"}, 400

        db.session.commit()
        return {"message": f"Timer {action}d for task {task_id}", "task": task.to_dict()}, 200

# Add resources to the API
api.add_resource(TaskList, "/tasks")
api.add_resource(StartTimer, "/start_timer")


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

# ---------------------
# App Entry Point
# ---------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensures tables are created for the first time
    app.run(debug=True)
