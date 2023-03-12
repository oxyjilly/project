#import os
from datetime import date, datetime
import sqlite3
#from tempfile import mkdtemp
from flask import Flask, redirect, render_template, request, session, url_for
#from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

#configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies), set a secret key for the session and security
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'myveryverysuper8secret2387key'
#Session(app)

# extracting current year and date
today = date.today()

currentMonth = today.month
currentYear = today.year

# connected to the database and creating the tables

conn = sqlite3.connect("journal.db", check_same_thread=False)
db = conn.cursor()

db.execute("CREATE TABLE if not exists users (username TEXT PRIMARY KEY, name TEXT, hash TEXT, tags INTEGER)")
db.execute("CREATE TABLE IF NOT EXISTS entry (entryId INTEGER PRIMARY KEY, username TEXT, date TEXT, text TEXT, FOREIGN KEY (username) REFERENCES users(username))")
db.execute("CREATE TABLE IF NOT EXISTS tags (tagId INTEGER PRIMARY KEY, tagName TEXT, username TEXT, FOREIGN KEY (username) REFERENCES users(username))")
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

        # get the hash password using cursor to compare later on
        hash = db.execute("SELECT hash FROM users WHERE username = ?", [request.form.get("username")])
        hashy = db.fetchone()
        hashyy = hashy[0]

        if not check_password_hash(hashyy, request.form.get("password")):
            apologyy = "Invalid password!"
            return render_template("apology.html", apology=apologyy)

        # Remember which user has logged in using the username
        session["user_id"] = request.form.get("username")


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

#the main route (calendar route), accepts month and year as parameters, the defualts are set earlier as the current year
# and month. These are used to find the calendar for that month and year using the calendar python inport

@app.route("/main", methods=["GET", "POST"])
def main(year=currentYear, month=currentMonth):
    if request.method == "POST":
        # IF submit new tag is clicked:
        newTag = request.form.get("newTag")
        print(newTag)
        username = session["user_id"]
        
        db.execute("INSERT INTO tags (tagName, userntagNameame) VALUES (?,?)", [newTag, username])
        conn.commit()
        return redirect("/main")
    
    else:
        # extracting current year and date
        # now = datetime.now()
        # month_name = now.strftime('%B')
        # month = today.month
        # year = now.year

        username = session["user_id"]
        name = db.execute("SELECT name FROM users WHERE username = ?", [username]).fetchone()[0]

        if month == 12:
            nextMonth = 1
            nextYear = year + 1
        else:
            nextMonth = month + 1
            nextYear = year

        if month == 1:
            prevMonth = 12
            prevYear = year - 1
        else:
            prevMonth = month - 1
            prevYear = year
        
        import calendar

        # Get the calendar for the specified year and month
        cal = calendar.monthcalendar(year, month)

        # Define the names of the months
        month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December']

        # Define the names of the days of the week
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        # Create a list of lists containing the calendar data
        calendar_data = []
        for week in cal:
            week_data = []
            for day in week:
                if day == 0:
                    week_data.append(None)
                else:
                    week_data.append(day)
            calendar_data.append(week_data)

        month_name = calendar.month_name[month]

        # the TAG section on the right hand side
        rows = db.execute("SELECT tagName FROM tags WHERE username = ?", [username]).fetchall()

        #loop through all tag names and add them to dict rows
        tagName = []
        for row in rows:
            tagName.append(row[0])


        return render_template('main.html', month_names=month_names, month_name=month_name, year=year, day_name=day_names, 
                                calendar=calendar_data, isEntry=isEntry, prevMonth=prevMonth, prevYear=prevYear, nextMonth=nextMonth, nextYear=nextYear, name=name,
                                tagName=tagName)


@app.route("/switchMonth", methods=["POST"])
def switch():

    if "nextMonth" in request.form:
        monthNow = request.form["currentMonth"]
        yearNow = request.form.get("currentYear")

        print(monthNow)
        print(yearNow)

        if monthNow == 12:
            newMonth = 1
            newYear = yearNow =+ 1
        else:
            newMonth = monthNow =+ 1
            newYear = yearNow

    if "previousMonth" in request.form:
        if monthNow == 1:
            newMonth = 12
            newYear = yearNow =- 1
        else:
            newMonth = monthNow =- 1
            newYear = yearNow

    print("newmonth: ", newMonth)
    print("newYear :", newYear)

    return redirect(url_for('main', year=int(newYear), month=int(newMonth)))


#main route which shows the user the info for the date that they clicked
@app.route("/event/<int:year>/<string:month>/<int:day>")
def event(year, month, day):
    apology = "you did something????? "
    print("year: ", year, "month and day: ", month, day)
    return render_template("apology.html", apology=apology)


# a function used to check if a date has any entries, so this can be displayed in the calendar
def isEntry(year, month_name, day):
    month_dict = {
    "January": "01",
    "February":"02",
    "March": "03",
    "April": "04",
    "May": "05",
    "June": "06",
    "July": "07",
    "August": "08",
    "September": "09",
    "October": "10",
    "November": "11",
    "December": "12"
    }

    monthDay = month_dict[month_name]

    #since the day is single digit, change it so it is 03 instead of 3
    if day < 10:
        theDay = "0" + str(day)
    else:
        theDay = day

    theDate = str(year) + "-" + str(monthDay) + "-" + str(theDay) 
    print("theDate is: ", theDate)

    username = session["user_id"]

    rows = db.execute("SELECT * FROM entry WHERE username = (?) AND date = (?)", [username, theDate])
    row = db.fetchone()
    print("rows: ", rows)
    print("row: ", row)
    if row is not None:
        return True 
    else:
        return False    



#make the route for a user submitting a newEntry
@app.route("/newEntry", methods=["GET", "POST"])
def newEntry():
    # if request.form.get("action") == "newEntrySubmitButton":
    # User reached route via GET (by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("newEntry.html", date=today)

    else: 
        userId = session["user_id"]
        entry = request.form.get("newEntryText")
        date = today

        #return render_template("apology.html", apology=entry)

        db.execute("INSERT INTO entry (username, text, date) VALUES (?,?,?)", [userId, entry, date])
        conn.commit()

        return redirect("/main")



# a route that ...
@app.route("/tag", methods=["GET", "POST"])
def tag():
    if request.method=="POST":
        tag = request.form.get("selectedTag")
        username = session["user_id"]
        
        tagRows = db.execute("SELECT * FROM entry WHERE entryId = (SELECT entryId FROM entryTag WHERE tagId = (SELECT tagId FROM tags WHERE tagName = (?) AND username = (?)))", [tag, username]).fetchall()
        
        tags = []
        for row in tagRows:
            data = {"entryId": row[0], 'username': row[1], 'date': row[2], 'text': row[3]}
            tags.append(data)

        return render_template("tags.html", tags=tags, tag=tag)

    





#main route which shows the calendar with the current dates
@app.route("/")
def showCalendar():
    return redirect("/login")

#route which logs out the user and forgets their session and username
@app.route("/logout")
def logout():

    # Forget any user_id / username
    session.clear()

    # Redirect user to login form
    return redirect("/")

