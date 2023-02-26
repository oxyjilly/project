import os
from flask import Flask, request
import sqlite3
from datetime import datetime

#configure application
app = Flask(__name__)

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


