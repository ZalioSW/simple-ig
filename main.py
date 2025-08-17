from flask import Flask, session, redirect, url_for, request, render_template
from tinydb import TinyDB, Query
import os
from werkzeug.utils import secure_filename
app = Flask(__name__)

db = TinyDB('ig.json')
users = db.table("users")
posts = db.table("posts")
upload_folder = "static/uploads"
os.makedirs(upload_folder, exist_ok=True)

app.secret_key = "zaliosw_najjaci123"
app.config["upload_folder"] = upload_folder

@app.route("/")
def hello_world():
    if "username" not in session:
        return redirect("/signup")
    data = posts.all()
    print(data)
    return render_template("index.html", username=session["username"], data=data)

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
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        User = Query()
        user = users.search((User.username == username) & (User.password == password))
        if user:
            session["username"] = username
            return redirect("/")
        else:
            error = "invalid credentials"
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect("/login")

@app.route("/upload", methods=[ "GET", "POST"])
def upload():
    error = None
    newId = len(posts) + 1
    if request.method == "POST":
        name = request.form["name"]
        image = request.files["image"]
        if image and name:
            imgname = secure_filename(image.filename)
            imgpath = os.path.join(app.config["upload_folder"], imgname).replace("\\", "/")
            image.save(imgpath)
            posts.insert({"id": newId, "user": session["username"], "name": name, "path": imgpath})
            return redirect("/")
        else:
            error = "Please select your file and input the name!"
    return render_template("upload.html", error=error)

@app.route("/viewProfile/<string:username>")
def viewProfile(username):
    if "username" not in session:
        return redirect("/signup")
    Post = Query()
    user_posts = posts.search(Post.user == username)
    return render_template("viewProfile.html", username=username, posts=user_posts)

@app.route("/likePost", methods=["POST"])
def likePost():
    username = request.form.get("username")
    post_id = int(request.form.get("post_id"))
    Post = Query()
    thePost = posts.get(Post.id == post_id)

    if thePost:
        if "likes" not in thePost:
            thePost["likes"] = []
        if username in thePost["likes"]:
            thePost["likes"].remove(username)
        else:
            thePost["likes"].append(username)
    posts.update({"likes": thePost["likes"]}, Post.id == post_id)

    return "OK", 200


    


app.run(debug=True)  