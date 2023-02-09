import os
from flask import Flask, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route("/newEntry", methods=["GET", "POST"])
def submittedEntry():
    if request.form.get("action") == "newEntrySubmitButton":
        
@app.route("/")
#Calendar
    #extracting current year and date

current_datetime = datetime.now()
current_month = current_datetime.month
current_year = current_datetime.year

print("hello world")


