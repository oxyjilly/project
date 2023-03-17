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

db.execute("CREATE TABLE if not exists users (username TEXT PRIMARY KEY, name TEXT, hash TEXT)")
db.execute("CREATE TABLE IF NOT EXISTS entry (entryId INTEGER PRIMARY KEY, username TEXT, date TEXT, title TEXT, text TEXT, tagName TEXT, FOREIGN KEY (username) REFERENCES users(username),  FOREIGN KEY (tagName) REFERENCES tags(tagName))")
db.execute("CREATE TABLE IF NOT EXISTS tags (tagId INTEGER PRIMARY KEY, tagName TEXT, username TEXT, FOREIGN KEY (username) REFERENCES users(username))")

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

        newUser = db.execute("INSERT INTO users(name, username, hash) VALUES(?,?,?)", [nameIn, usernameIn, generate_password_hash(passwordIn)])
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
def main():
    if request.method == "POST":
        # importing the global variables so can cchange them and then use the new values
        global currentYear
        global currentMonth

        # IF submit new tag is clicked (PART of the main screen), add the new tag into db:
        if "newTag" in request.form:
            newTag = request.form.get("newTag")
            username = session["user_id"]
        
            # adding new tag into ´tags´ table
            db.execute("INSERT INTO tags (tagName, username) VALUES (?,?)", [newTag, username])
            conn.commit()

        if "nextMonth" or "prevMonth" in request.form:

            # TO SWITCH MONTH, when next or prev is clicked, this execut4es
            # get the current values for next montha and prev month using if 
            if "nextMonth" in request.form:
                monthNow = request.form.get("nextMonth")
                year = request.form.get("currentYear")

                if monthNow == 1:
                    yearNow = year + 1
                else:
                    yearNow = year

                currentMonth = monthNow
                currentYear = yearNow


            if "prevMonth" in request.form:
                monthNow = request.form.get("prevMonth")
                year = request.form.get("currentYear")

                if monthNow == 12:
                    yearNow = year - 1
                else:
                    yearNow = year
                
                currentMonth = monthNow
                currentYear = yearNow

        return redirect("/main")
    
    else:
        # extracting current year and date
        # now = datetime.now()
        # month_name = now.strftime('%B')
        # month = today.month
        # year = now.year

        month = int(currentMonth)
        year = int(currentYear)

        print("the SECOND MAIN curretn month is : ", currentMonth)

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

        #find length of tagName to see if it is empty (so user has no tags)
        tagLen = len(tagName)


        return render_template('main.html', month_names=month_names, month_name=month_name, year=year, day_name=day_names, calendar=calendar_data, isEntry=isEntry, prevMonth=prevMonth, prevYear=prevYear, nextMonth=nextMonth, nextYear=nextYear, name=name, tagName=tagName, tagLen=tagLen)

'''
FIX PLS YOU CANT HAVE A CALENDAR WITH ONLY ONE MONTH STUPID
@app.route("/switchMonth", methods=["POST"])
def switch():

    # get the current values for next montha and prev month using if 
    if "nextMonth" in request.form:
        monthNow = request.form.get("nextMonth")
        year = request.form.get("currentYear")

        if monthNow == 1:
            yearNow = year + 1
        else:
            yearNow = year

    if "prevMonth" in request.form:
        monthNow = request.form.get("prevMonth")
        year = request.form.get("currentYear")

        if monthNow == 12:
            yearNow = year - 1
        else:
            yearNow = year
        

    print("month NOW IS: ", monthNow)
    print("year NOW IS : ", yearNow)

    currentMonth = monthNow
    currentYear = yearNow

    return redirect("/main")
'''

#main route which shows the user the info for the date that they clicked
@app.route("/event/<int:year>/<string:month>/<int:day>")
def event(year, month, day):

    #convert month name into month day: 
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

    monthDay = month_dict[month]

    conDate = str(year) + "-" + str(monthDay) + "-" + str(day)

    username = session["user_id"]
    print(conDate)
    entries = db.execute("SELECT title, text FROM entry WHERE date = (?) AND username = (?)", [conDate, username]).fetchall()

    print("the entries db is: ", entries)
    dateEntries = []
    for entry in entries:
        dateEntries.append({"title": entry[0], "text": entry[1]})

    print("dateEntries isss: ", dateEntries)

    return render_template("event.html", date=conDate, entries=dateEntries)


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

    username = session["user_id"]

    rows = db.execute("SELECT * FROM entry WHERE username = (?) AND date = (?)", [username, theDate])
    row = db.fetchone()
    
    #print("rows: ", rows)
    #print("row: ", row)
    
    if row is not None:
        return True 
    else:
        return False    



#make the route for a user submitting a newEntry
@app.route("/newEntry", methods=["GET", "POST"])
def newEntry():
    # User reached route via GET (by clicking a link or via redirect)
    if request.method == "GET":

        userId = session["user_id"]
        tagRows = db.execute("SELECT tagName from tags WHERE username = ?", [userId]).fetchall()

         #loop through all tag names and add them to dict tagsAvail
        tagsAvail = []
        for row in tagRows:
            tagsAvail.append(row[0])

        return render_template("newEntry.html", date=today, tagsAvail=tagsAvail)

    else: 
        userId = session["user_id"]
        entry = request.form.get("newEntryText")
        title = request.form.get("newTitleText")
        date = today

        #get the tag selected by user
        taggg = request.form.get("tagAvail")
        print("tagggggg is: ", taggg)

        db.execute("INSERT INTO entry (username, title, text, date, tagName) VALUES (?,?,?,?,?)", [userId, title, entry, date, taggg])
        conn.commit()

        return redirect("/main")



# a route that ...
@app.route("/tag", methods=["GET", "POST"])
def tag():
    if request.method=="POST":
        #find the tagName that user (using their username) selected, find all entries which have that tag tagged in query
        tagName = request.form.get("selectedTag")
        username = session["user_id"]
        
        tagRows = db.execute("SELECT date, title, text FROM entry WHERE tagName = (?) AND username = (?)", [tagName, username]).fetchall()
        #tagText = db.execute("SELECT text FROM entry WHERE tagName= (?) AND username = (?)", [tagName, username]).fetchall()

        print("the TAGROWS IS: ", tagRows)
        tags = []
        for row in tagRows:
            data = {"date": row[0], "title": row[1], "text": row[2]}
            tags.append(data)
        print("tags dict is: ", tags)

        return render_template("tags.html", tags=tags, tagName=tagName)



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