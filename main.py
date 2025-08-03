from flask import Flask, session, redirect, url_for, request, render_template
from tinydb import TinyDB, Query
app = Flask(__name__)

db = TinyDB('ig.json')
users = db.table("users")
posts = db.table("posts")

app.secret_key = "zaliosw_najjaci123"

@app.route("/")
def hello_world():
    if "username" not in session:
        return redirect("/signup")
    return render_template("index.html", username=session["username"])

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        users.insert({"username": username, "password": password})
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        print(username)
        print(password)
        User = Query()
        user = users.search((User.username == username) & (User.password == password))
        print(user)
        if user:
            session["username"] = username
            return redirect("/")
        else:
            return "<p>Neki je narobe</p>"
    return render_template("login.html")

app.run(debug=True)  