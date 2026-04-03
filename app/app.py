from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this in production

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Simple in-memory user storage
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

users = []

@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user.id == int(user_id):
            return user
    return None

tasks = []
task_id = 1

@app.route("/")
@login_required
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password")
        
        if not username:
            flash("Username cannot be empty")
            return render_template("login.html")
        
        if not password:
            flash("Password cannot be empty")
            return render_template("login.html")
        
        # Check password
        if password != "passat":
            flash("Invalid password")
            return render_template("login.html")

        # Search for existing user
        for user in users:
            if user.username == username:
                login_user(user)
                return redirect(url_for("home"))

        # Create new user on the fly if not found
        next_id = max([u.id for u in users], default=0) + 1
        new_user = User(next_id, username)
        users.append(new_user)
        login_user(new_user)
        return redirect(url_for("home"))

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/members")
@login_required
def members():
    return render_template("members.html", users=users)

@app.route("/api/tasks", methods=["GET"])
@login_required
def get_tasks():
    return jsonify(tasks)

@app.route("/api/tasks", methods=["POST"])
@login_required
def add_task():
    global task_id
    data = request.json
    
    # Walidacja priorytetu
    priority = data.get("priority", "Średni")
    if priority not in ["Niski", "Średni", "Wysoki"]:
        priority = "Średni"

    task = {
        "id": task_id,
        "title": data.get("title"),
        "priority": priority,
        "done": False,
        "user": current_user.username,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    tasks.append(task)
    task_id += 1

    return jsonify(task), 201

@app.route("/api/tasks/<int:id>", methods=["PUT"])
@login_required
def update_task(id):
    data = request.json
    for task in tasks:
        if task["id"] == id:
            task["done"] = data.get("done", task["done"])
            
            # Walidacja priorytetu
            if "priority" in data:
                priority = data.get("priority")
                if priority in ["Niski", "Średni", "Wysoki"]:
                    task["priority"] = priority
            
            return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

@app.route("/api/tasks/<int:id>", methods=["DELETE"])
@login_required
def delete_task(id):
    global tasks
    tasks = [t for t in tasks if t["id"] != id]
    return jsonify({"message": "deleted"})

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)