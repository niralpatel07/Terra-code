from flask import Flask, render_template, request, redirect 

app = Flask(__name__)

tasks = [
    {"id": 1, "text": "Finish School Homework", "done": False},
    {"id": 2, "text": "Lock in for DECA", "done": False},
    {"id": 3, "text": "Code for Terra", "done": False},
]
next_id = 4

@app.route("/", methods=["GET", "POST"])
def home():
    global next_id
    if request.method == "POST":
        text = request.form["task"].strip()
        existing = [t["text"] for t in tasks]
        if text != "" and text not in existing and len(text) <= 60:
            tasks.append({"id": next_id, "text": text, "done": False})
            next_id += 1
        return redirect("/")
    return render_template("index.html", tasks=tasks, editing_id=None) 

@app.route("/done/<int:task_id>", methods=["POST"])
def done(task_id):
    for t in tasks:
        if t["id"] == task_id:
            t["done"] =  not t["done"]
    return redirect("/")

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return redirect("/")

@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit(task_id):
    if request.method == "POST":
        new_text = request.form["task"].strip()
        for t in tasks:
            if t["id"] == task_id and new_text != "" and len(new_text) <= 60:
                t["text"] = new_text
        return redirect("/")
    return render_template("index.html", tasks=tasks, editing_id=task_id)

@app.route("/clear", methods=["POST"])
def clear():
    tasks.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
