import json
import os
from datetime import date

from flask import Flask, render_template, request, redirect 

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

DEFAULT_TASKS = [
    {"id": 1, "text": "Finish School Homework", "done": False, "priority": "high"},
    {"id": 2, "text": "Lock in for DECA", "done": False, "priority": "medium"},
    {"id": 3, "text": "Code for Terra", "done": False, "priority": "low"},
]

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        return data["tasks"], data["next_id"]
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return [dict(t) for t in DEFAULT_TASKS], 4

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump({"tasks": tasks, "next_id": next_id}, f, indent=4)

tasks, next_id = load_data()

def sorted_tasks():
    return sorted(tasks, key=lambda t: (t["done"], PRIORITY_ORDER.get(t["priority"], 1)))

@app.route("/", methods=["GET", "POST"])
def home():
    global next_id
    if request.method == "POST":
        text = request.form["task"].strip()
        priority = request.form.get("priority", "medium")
        if priority not in PRIORITY_ORDER:
            priority = "medium" 
        existing = [t["text"] for t in tasks]
        if text != "" and text not in existing and len(text) <= 60:
            tasks.append({
                "id": next_id,
                "text": text,
                "done": False,
                "priority": priority,
                "created": date.today().isoformat(),
            }) 
            next_id += 1
            save_data()
        return redirect("/")
    return render_template("index.html", tasks=sorted_tasks(), editing_id=None) 

@app.route("/done/<int:task_id>", methods=["POST"])
def done(task_id):
    for t in tasks:
        if t["id"] == task_id:
            t["done"] =  not t["done"]
    save_data()
    return redirect("/")

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    save_data()
    return redirect("/")

@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit(task_id):
    if request.method == "POST":
        new_text = request.form["task"].strip()
        for t in tasks:
            if t["id"] == task_id and new_text != "" and len(new_text) <= 60:
                t["text"] = new_text
        save_data()
        return redirect("/")
    return render_template("index.html", tasks=sorted_tasks(), editing_id=task_id)

@app.route("/clear-done", methods=["POST"])
def clear_done():
    global tasks
    tasks = [t for t in tasks if not t["done"]]
    save_data()
    return redirect("/")

@app.route("/clear", methods=["POST"])
def clear():
    tasks.clear()
    save_data()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True) 