from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

SPORTS = ["Basketball", "Soccer", "Ultimate frisbee"]

con = sqlite3.connect("registrants.db", check_same_thread=False)
cur = con.cursor()

@app.route("/")
def index():
    return render_template("index.html", sports=SPORTS)

@app.route("/deregister", methods=["POST"])
def deregister():
    id = request.form.get("id")
    if id:
        cur.execute("DELETE FROM table1 WHERE id = ?", id)
        con.commit()
    return redirect("/registrants")

@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    sport = request.form.get("sport")
    if not name or sport not in SPORTS:
        return render_template("failure.html")
    cur.execute("INSERT INTO table1(name, sport) VALUES(?, ?)", [name, sport])
    con.commit()
    return redirect("/registrants")

@app.route("/registrants")
def registrants():
    cur.execute("SELECT * FROM table1")
    registrants = cur.fetchall()
    return render_template("registrants.html", registrants=registrants)