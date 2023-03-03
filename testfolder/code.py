import os
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

#configure application
app = Flask(__name__)

# connected to the database and creating the tables 
conn = sqlite3.connect("journal.db")
db = conn.cursor()

db.execute("CREATE TABLE if not exists users (userId INTEGER PRIMARY KEY, name TEXT, username TEXT, hash TEXT, tags INTEGER)")

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

        # error message if there is: 1. no username entered 2. no password entered 3. no name entered
        if not request.form.get("username"):
            # TODO

        elif not request.form.get("password") or not request.form.get("confirmation"):
            # TODO

        elif request.form.get("password") != request.form.get("confirmation"):
            # TODO
        
        elif not request.form.get("name"):
            # TODO

        # if there is a username that's the same as the one user registered with, its compared to any username from the database
        usernameIn = request.form.get("username")
        passwordIn = request.form.get("password")

        rows = db.execute("SELECT * FROM users WHERE username = ?", usernameIn)

        if len(rows) != 0:
            return apology("this username already exists, pick another please", 400)

        newUser = db.execute("INSERT INTO users(username, hash) VALUES(?,?)", usernameIn, generate_password_hash(passwordIn))

        session["user_id"] = newUser

        # Redirect user to home page
        return redirect("/")

    


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


