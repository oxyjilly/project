import os
from flask import Flask, flash, redirect, render_template, request, session
#from flask_session import Session
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

#configure application
app = Flask(__name__)

# connected to the database and creating the tables 
conn = sqlite3.connect("journal.db")
db = conn.cursor()

db.execute("CREATE TABLE if not exists users (userId INTEGER PRIMARY KEY, name TEXT, username TEXT, hash TEXT, tags INTEGER)")
db.execute("CREATE TABLE IF NOT EXISTS entry (entryId INTEGER PRIMARY KEY, userId INTEGER, date DATE, text TEXT")
db.execute("CREATE TABLE IF NOT EXISTS entryTag (id INTEGER PRIMARY KEY, entryId INTEGER FOREIGN KEY, tagId INTEGER FOREIGN KEY)")

db.commit()

# an app route to allow user to register (from the register.html page)
@app.route("/register", methods=["GET", "POST"])
def register():

    session.clear()

    # user clicked on 'register', so it loads the register.html page (thru GET), when they click 'submit' it will be request.method post (see below)
    if request.method == "GET":
        return render_template("register.html")

    # User reached route via POST (by pressing 'submit' on the register.html page)
    else:

        # error message if there is: 1. no username entered 2. no password entered 
        # 3. password and confirmation don't match 4. no name entered

        # the 'apology' is a string, which is then pushed to apology.html using render_template, 
        # in apology.html it is shown to the user by using Jinga
        if not request.form.get("username"):
            apology = "No username entered!"
            return render_template("apology.html", apology=apology)

        elif not request.form.get("password") or not request.form.get("confirmation"):
            apology = "No password or confirmation entered!"
            return render_template("apology.html", apology=apology)

        elif request.form.get("password") != request.form.get("confirmation"):
            apology = "Password does not match confirmation!"
            return render_template("apology.html", apology=apology)
        
        elif not request.form.get("name"):
            apology = "No name entered!"
            return render_template("apology.html", apology=apology)

        # if there is a username that's the same as the one user registered with, its compared to any username from the database
        nameIn = request.form.get("name")
        usernameIn = request.form.get("username")
        passwordIn = request.form.get("password")

        rows = db.execute("SELECT * FROM users WHERE username = ?", usernameIn)

        if len(rows) != 0:
            apology = "This username already exists, pick another please!"
            return render_template("apology.html", apology=apology)

        newUser = db.execute("INSERT INTO users(name, username, hash, tags) VALUES(?,?,?,?)", nameIn, usernameIn, generate_password_hash(passwordIn), 0)
        db.commit()

        # establish the session user id
        session["user_id"] = newUser.lastrowid

        # Redirect user to home page
        return redirect("/main.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            apology = "No username entered!"
            return render_template("apology.html", apology=apology)

        # Ensure password was submitted
        elif not request.form.get("password"):
            apology = "No password entered!"
            return render_template("apology.html", apology=apology)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            apology = "Invalid username and/or password!"
            return render_template("apology.html", apology=apology)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/main.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")



#make the route for a user submitting a newEntry
@app.route("/newEntry", methods=["GET", "POST"])
def submittedEntry():
    #if request.form.get("action") == "newEntrySubmitButton":
    print("hello")
        

#main route which shows the calendar with the current dates
@app.route("/")
def showCalendar():
    #extracting current year and date
    current_datetime = datetime.now()
    current_month = current_datetime.month
    current_year = current_datetime.year


