from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

tasks = []
task_id = 1

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)

@app.route("/api/tasks", methods=["POST"])
def add_task():
    global task_id
    data = request.json

    task = {
        "id": task_id,
        "title": data.get("title"),
        "done": False
    }

    tasks.append(task)
    task_id += 1

    return jsonify(task), 201

@app.route("/api/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    data = request.json
    for task in tasks:
        if task["id"] == id:
            task["done"] = data.get("done", task["done"])
            return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

@app.route("/api/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    global tasks
    tasks = [t for t in tasks if t["id"] != id]
    return jsonify({"message": "deleted"})

@app.route("/health")
def health():
    return {"status": "ok"}


app.run(host="0.0.0.0", port=5000)