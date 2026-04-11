from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# -------- DATABASE --------
def get_db():
    return sqlite3.connect("trees.db")

def init_db():
    con = get_db()
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS volunteers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS trees(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        volunteer TEXT,
        tree_name TEXT,
        location TEXT,
        growth TEXT
    )
    """)

    con.commit()
    con.close()

init_db()

# -------- ROUTES --------

# Register page
@app.route("/")
def home():
    return render_template("register.html")

# Register volunteer
@app.route("/register", methods=["POST"])
def register():
    name = request.form["name"]
    email = request.form["email"]

    con = get_db()
    cur = con.cursor()
    cur.execute("INSERT INTO volunteers (name, email) VALUES (?,?)", (name, email))
    con.commit()
    con.close()

    return redirect(url_for("dashboard"))

# Dashboard
@app.route("/dashboard")
def dashboard():
    con = get_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM trees")
    trees = cur.fetchall()
    con.close()

    return render_template("dashboard.html", trees=trees)

# Add Tree Page
@app.route("/add_tree_page")
def add_tree_page():
    return render_template("add_tree.html")

# Add Tree Record
@app.route("/add_tree", methods=["POST"])
def add_tree():
    volunteer = request.form["volunteer"]
    tree_name = request.form["tree_name"]
    location = request.form["location"]
    growth = request.form["growth"]

    con = get_db()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO trees (volunteer, tree_name, location, growth) VALUES (?,?,?,?)",
        (volunteer, tree_name, location, growth)
    )
    con.commit()
    con.close()

    return redirect(url_for("dashboard"))

# Delete Tree
@app.route("/delete/<int:id>")
def delete(id):
    con = get_db()
    cur = con.cursor()
    cur.execute("DELETE FROM trees WHERE id=?", (id,))
    con.commit()
    con.close()

    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True)