from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

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


def normalize_priority(value):
    mapping = {
        "Niski": "Low",
        "Średni": "Medium",
        "Wysoki": "High"
    }
    normalized = mapping.get(value, value)
    if normalized not in ["Low", "Medium", "High"]:
        return "Medium"
    return normalized


def normalize_recurrence(value):
    allowed = ["none", "daily", "weekly", "monthly"]
    if value in allowed:
        return value
    return "none"


def normalize_tags(value):
    if isinstance(value, list):
        raw_tags = value
    elif isinstance(value, str):
        raw_tags = value.split(",")
    else:
        raw_tags = []

    cleaned = []
    seen = set()
    for tag in raw_tags:
        tag_str = str(tag).strip()
        if not tag_str:
            continue
        tag_key = tag_str.lower()
        if tag_key in seen:
            continue
        seen.add(tag_key)
        cleaned.append(tag_str)
    return cleaned


def normalize_due_date(raw_due_date):
    if not raw_due_date:
        return None
    try:
        datetime.strptime(raw_due_date, "%Y-%m-%d")
        return raw_due_date
    except ValueError:
        return None


def ensure_task_defaults(task):
    task["priority"] = normalize_priority(task.get("priority", "Medium"))
    task["project"] = str(task.get("project", "General") or "General").strip() or "General"
    task["tags"] = normalize_tags(task.get("tags", []))
    task["recurrence"] = normalize_recurrence(task.get("recurrence", "none"))
    task["attachment_url"] = (task.get("attachment_url") or "").strip() or None
    task["comments"] = task.get("comments") if isinstance(task.get("comments"), list) else []
    task["due_date"] = normalize_due_date(task.get("due_date"))
    task["parent_task_id"] = task.get("parent_task_id")
    return task


def compute_next_due_date(task):
    recurrence = task.get("recurrence", "none")
    if recurrence == "none":
        return None

    base_str = task.get("due_date")
    if base_str:
        try:
            base_date = datetime.strptime(base_str, "%Y-%m-%d").date()
        except ValueError:
            base_date = datetime.now().date()
    else:
        base_date = datetime.now().date()

    if recurrence == "daily":
        return (base_date + timedelta(days=1)).strftime("%Y-%m-%d")
    if recurrence == "weekly":
        return (base_date + timedelta(days=7)).strftime("%Y-%m-%d")
    if recurrence == "monthly":
        year = base_date.year
        month = base_date.month + 1
        if month > 12:
            month = 1
            year += 1

        first_next_next_month = datetime(year + (1 if month == 12 else 0), 1 if month == 12 else month + 1, 1)
        last_day_target = (first_next_next_month - timedelta(days=1)).day
        day = min(base_date.day, last_day_target)
        return datetime(year, month, day).strftime("%Y-%m-%d")

    return None


def create_recurring_task(source_task):
    global task_id

    next_due_date = compute_next_due_date(source_task)
    if not next_due_date:
        return None

    next_task = {
        "id": task_id,
        "title": source_task.get("title"),
        "priority": source_task.get("priority", "Medium"),
        "done": False,
        "user": source_task.get("user", current_user.username),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "due_date": next_due_date,
        "completed_at": None,
        "completed_by": None,
        "project": source_task.get("project", "General"),
        "tags": list(source_task.get("tags", [])),
        "recurrence": source_task.get("recurrence", "none"),
        "attachment_url": source_task.get("attachment_url"),
        "comments": [],
        "parent_task_id": source_task.get("id")
    }

    tasks.append(ensure_task_defaults(next_task))
    task_id += 1
    return next_task

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
        
        if password != "passat":
            flash("Invalid password")
            return render_template("login.html")

        for user in users:
            if user.username == username:
                login_user(user)
                return redirect(url_for("home"))

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
    completed_by_user = {
        user.username: [task for task in tasks if task.get("completed_by") == user.username]
        for user in users
    }
    return render_template("members.html", users=users, completed_by_user=completed_by_user)

@app.route("/api/tasks", methods=["GET"])
@login_required
def get_tasks():
    for task in tasks:
        ensure_task_defaults(task)
    return jsonify(tasks)

@app.route("/api/tasks", methods=["POST"])
@login_required
def add_task():
    global task_id
    data = request.json or {}

    title = str(data.get("title", "")).strip()
    if not title:
        return jsonify({"error": "Task title is required"}), 400

    priority = normalize_priority(data.get("priority", "Medium"))
    due_date = normalize_due_date(data.get("due_date"))
    project = str(data.get("project", "General") or "General").strip() or "General"
    tags = normalize_tags(data.get("tags", []))
    recurrence = normalize_recurrence(data.get("recurrence", "none"))
    attachment_url = (data.get("attachment_url") or "").strip() or None

    comments = []
    initial_note = str(data.get("initial_note", "")).strip()
    if initial_note:
        comments.append({
            "id": 1,
            "text": initial_note,
            "author": current_user.username,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    task = {
        "id": task_id,
        "title": title,
        "priority": priority,
        "done": False,
        "user": current_user.username,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "due_date": due_date,
        "completed_at": None,
        "completed_by": None,
        "project": project,
        "tags": tags,
        "recurrence": recurrence,
        "attachment_url": attachment_url,
        "comments": comments,
        "parent_task_id": None
    }

    tasks.append(ensure_task_defaults(task))
    task_id += 1

    return jsonify(task), 201

@app.route("/api/tasks/<int:id>", methods=["PUT"])
@login_required
def update_task(id):
    data = request.json or {}
    for task in tasks:
        if task["id"] == id:
            ensure_task_defaults(task)
            was_done = task.get("done", False)
            task["done"] = data.get("done", task["done"])

            if task["done"]:
                task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                task["completed_by"] = current_user.username
            else:
                task["completed_at"] = None
                task["completed_by"] = None

            if "priority" in data:
                task["priority"] = normalize_priority(data.get("priority"))

            if "due_date" in data:
                task["due_date"] = normalize_due_date(data.get("due_date"))

            if "title" in data:
                title = str(data.get("title", "")).strip()
                if title:
                    task["title"] = title

            if "project" in data:
                task["project"] = str(data.get("project", "General") or "General").strip() or "General"

            if "tags" in data:
                task["tags"] = normalize_tags(data.get("tags", []))

            if "recurrence" in data:
                task["recurrence"] = normalize_recurrence(data.get("recurrence"))

            if "attachment_url" in data:
                task["attachment_url"] = (data.get("attachment_url") or "").strip() or None

            if "comment" in data:
                comment_text = str(data.get("comment", "")).strip()
                if comment_text:
                    next_comment_id = max([c.get("id", 0) for c in task["comments"]], default=0) + 1
                    task["comments"].append({
                        "id": next_comment_id,
                        "text": comment_text,
                        "author": current_user.username,
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })

            if task["done"] and not was_done and task.get("recurrence") != "none":
                create_recurring_task(task)

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