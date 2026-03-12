from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret"

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        batch = request.form["batch"]

        conn = get_db()
        conn.execute("INSERT INTO alumni(name,email,batch) VALUES(?,?,?)",(name,email,batch))
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]

        conn = get_db()
        user = conn.execute("SELECT * FROM alumni WHERE email=?",(email,)).fetchone()
        conn.close()

        if user:
            session["user"] = user["name"]
            return redirect("/dashboard")

    return render_template("login.html")

@app.route("/dashboard", methods=["GET","POST"])
def dashboard():
    conn = get_db()

    if request.method == "POST":
        post = request.form["post"]
        conn.execute("INSERT INTO posts(content) VALUES(?)",(post,))
        conn.commit()

    posts = conn.execute("SELECT * FROM posts").fetchall()
    alumni = conn.execute("SELECT * FROM alumni").fetchall()

    conn.close()

    return render_template("dashboard.html",posts=posts,alumni=alumni)

if __name__ == "__main__":
    app.run(debug=True)