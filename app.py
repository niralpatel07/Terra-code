import json
import os
from datetime import date, datetime

from flask import Flask, render_template, request, redirect, jsonify 

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
        json.dump({"tasks": tasks, "next_id": next_id}, f, indent=2)

tasks, next_id = load_data()
SESSIONS_FILE = os.path.join(os.path.dirname(__file__), "sessions.json")

def load_sessions():
    try:
        with open(SESSIONS_FILE, "r") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_sessions():
    with open(SESSIONS_FILE, "w") as f:
        json.dump(sessions, f, indent=2)

sessions = load_sessions()

def today_stats():
    today = date.today().isoformat()
    todays = [s for s in sessions if s["date"] == today]
    return len(todays), sum(s["minutes"] for s in todays)

def visible_tasks(view, query):
    result = tasks 
    if view == "active":
        result = [t for t in result if not t["done"]]
    elif view == "done":
        result = [t for t in result if t["done"]]
    if query:
        result = [t for t in result if query.lower() in t["text"].lower()]
    return sorted(
        result,
        key=lambda t: (
            t["done"],
            PRIORITY_ORDER.get(t["priority"], 1),
            t.get("due") or "9999-12-31",
        ), 
    )

def render_page(editing_id=None):
    view = request.args.get("view", "all")
    query = request.args.get("q", "").strip()
    today = date.today().isoformat()
    overdue = sum(
        1 for t in tasks if t.get("due") and t["due"] < today and not t["done"]
    )
    return render_template(
        "index.html",
        tasks=visible_tasks(view, query),
        editing_id=editing_id,
        view=view,
        q=query,
        today=today,
        total=len(tasks),
        done_count=sum(1 for t in tasks if t["done"]),
        overdue=overdue,
    )

@app.route("/", methods=["GET", "POST"])
def home():
    global next_id
    if request.method == "POST":
        text = request.form["task"].strip()
        priority = request.form.get("priority", "medium")
        due = request.form.get("due", "")
        if priority not in PRIORITY_ORDER:
            priority = "medium" 
        existing = [t["text"] for t in tasks]
        if text != "" and text not in existing and len(text) <= 60:
            tasks.append({
                "id": next_id,
                "text": text,
                "done": False,
                "priority": priority,
                "due": due,
                "created": date.today().isoformat(),
            }) 
            next_id += 1
            save_data()
        return redirect("/")
    return render_page() 

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
    return render_page(editing_id=task_id)

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

@app.route("/timer")
def timer():
    count, minutes = today_stats()
    return render_template("timer.html", sessions_today=count, minutes_today=minutes)

@app.route("/log-session", methods=["POST"])
def log_session():
    data = request.get_json(silent=True) or {}
    try:
        minutes = int(data.get("minutes", 0))
    except (TypeError, ValueError):
        minutes = 0
    if minutes <= 0 or minutes > 180:
        return jsonify(error="bad minutes"), 400
    sessions.append({
        "date": date.today().isoformat(),
        "time": datetime.now().strftime("%H:%M:%S"),
        "minutes": minutes,
        "label": str(data.get("label", "")).strip()[:60]
    })

    save_sessions()
    count, total = today_stats()
    return jsonify(sessions_today=count, minutes_today=total)

if __name__ == "__main__":
    app.run(debug=True)