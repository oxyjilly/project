#import os
from datetime import datetime
import sqlite3
#from tempfile import mkdtemp
from flask import Flask, redirect, render_template, request, session
#from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

#configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies), set a secret key for the session and security
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'myveryverysuper8secret2387key'
#Session(app)

today = datetime.today()

# connected to the database and creating the tables

conn = sqlite3.connect("journal.db", check_same_thread=False)
db = conn.cursor()

db.execute("CREATE TABLE if not exists users (username TEXT PRIMARY KEY, name TEXT, hash TEXT, tags INTEGER)")
db.execute("CREATE TABLE IF NOT EXISTS entry (entryId INTEGER PRIMARY KEY, username TEXT, date TEXT, text TEXT, FOREIGN KEY (username) REFERENCES users(username))")
db.execute("CREATE TABLE IF NOT EXISTS tags (tagId INTEGER PRIMARY KEY, tagName TEXT)")
db.execute("CREATE TABLE IF NOT EXISTS entryTag (id INTEGER PRIMARY KEY, entryId INTEGER, tagId INTEGER, FOREIGN KEY (entryId) REFERENCES entry (entryId), FOREIGN KEY (tagId) REFERENCES tags(tagId))")

# an app route to allow user to register (from the register.html page)
@app.route("/register", methods=["GET", "POST"])
def register():

    # session.clear()

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
            apologyy = "No username entered!"
            return render_template("apology.html", apology=apologyy)

        if not request.form.get("password") or not request.form.get("confirmation"):
            apologyy = "No password or confirmation entered!"
            return render_template("apology.html", apology=apologyy)

        if request.form.get("password") != request.form.get("confirmation"):
            apologyy = "Password does not match confirmation!"
            return render_template("apology.html", apology=apologyy)

        if not request.form.get("name"):
            apologyy = "No name entered!"
            return render_template("apology.html", apology=apologyy)
        
        # if there is a username that's the same as the one user registered with, its compared to any username from the database
        nameIn = request.form.get("name")
        usernameIn = request.form.get("username")
        passwordIn = request.form.get("password")

        rows = db.execute("SELECT * FROM users WHERE username = ?", [usernameIn])
        print(rows)

        if rows.fetchone() is not None:
            # There are no rows for this query
            apologyy = "This username already exists, pick another please!"
            return render_template("apology.html", apology=apologyy)

        newUser = db.execute("INSERT INTO users(name, username, hash, tags) VALUES(?,?,?,?)", [nameIn, usernameIn, generate_password_hash(passwordIn), 0])
        conn.commit()

        # establish the session user id
        session["user_id"] = usernameIn

        # Redirect user to home page
        return redirect("/main")

@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            apologyy = "No username entered!"
            return render_template("apology.html", apology=apologyy)

        # Ensure password was submitted
        elif not request.form.get("password"):
            apologyy = "No password entered!"
            return render_template("apology.html", apology=apologyy)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", [request.form.get("username")])
        last_row = db.fetchone()

        # Ensure username exists and password is correct
        ############# something wrong with comparing hash and password even when its right #########
        if last_row is None:
            apologyy = "Invalid username"
            return render_template("apology.html", apology=apologyy)

        if not check_password_hash(last_row["hash"], request.form.get("password")):
            apologyy = "Invalid password!"
            return render_template("apology.html", apology=apologyy)


        # access the "username" column of the last row
        usernameValue = last_row["username"]

        # Remember which user has logged in
        session["user_id"] = usernameValue

        # Redirect user to home page
        return redirect("/main")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

#app route for apology .html
@app.route("/apology", methods=["GET", "POST"])
def apology():
    if request.method == "GET":
        return render_template("apology.html")

    return render_template("apology.html")

@app.route("/main", methods=["GET", "POST"])
def main():
    # User reached route via GET (by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("main.html")


#make the route for a user submitting a newEntry
@app.route("/newEntry", methods=["GET", "POST"])
def newEntry():
    # if request.form.get("action") == "newEntrySubmitButton":
    # User reached route via GET (by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("newEntry.html")

    else: 
        userId = session["user_id"]
        entry = request.form.get("newEntryText")
        date = today

        db.execute("INSERT INTO entry (username, text, date) VALUES (?,?,?)", (userId), (entry), (date))
        db.commit()



       
#main route which shows the calendar with the current dates
@app.route("/")
def showCalendar():
    # extracting current year and date
    # current_datetime = datetime.now()
    # current_month = current_datetime.month
    # current_year = current_datetime.year
    return render_template("template.html")

