# JOURNALIA
#### Video Demo: https://youtu.be/LcOT4cn35Qk 
#### Description:
My CS50 final project is a journalling website made primarily with Python and HTML. The idea for this project arose from the evident stress that the students in my high school were constantly facing due to exams and other pressures. There are many benefits to journalling, which is why I made a simple journalling website that can be used to de-stress. 
The main code for this website is written in app.py using Python and flask. First, a database with three tables is set up using SQLite, to make sure each journal entry is saved to the correct user. Below this are several routes that each perform a different task. The routes "register", "login", and "logout" use the relevant SQL tables and flask_session to register, login, or logout the user. 
The route "/newEntry" allows the user to submit a new journal entry, and saves this to the correct SQL tables. The route "/tag" displays all of the journal entries that have been saved under the tag that the user selected. The route "/view" displays the title and full text of any entry that the user clicked.
The main logic is written in the route "/main". The route adds new tags that the user has typed into the "add new tag" box into the SQL database. It also switches to the next or previous month corresponding to what the user clicked, including changing year after December or before January. This route also displays the correct dates for each month on a calendar-like layout.
To display all of this information to the user, flask's render_template is used in each route, to pass the information to the relevant HTML page. All of the HTML pages are stored under 'templates' and their names mostly correspond to what they do. Template.html contains the scripts and links of css and javascript, it also has a bootstrap script that displays a navigation bar with links to every page in the website. Using Jinja, this template is added to every other HTML page so the navigation bar is visible on every page.
Main.html is the main page the user sees when they login. It is rendered from the "/main" route in app.py, and has information passed to it from this route. This page displayes the main calendar view by using Jinja to loop through the dates of the relevant month and display them accurately in a table layout. The calendar display also calls the route "/isEntry" which determines if the user has posted an entry on a specific day, if True, this day is underlined as a link that the user can click to redirect them to a page where the entries for this date are shown.
The main page also has several forms that take information from the user and post it to the relevant route in app.py - such as switching the month is a form posted to '/main', and adding a new tag is a form posted to '/tag'. 
The other HTML pages follow a similar, simplified process and display the relevant information that has been passed to them from the routes in app.py. 
styles.css contains css that makes the website more aesthetically pleasing, such as by having round buttons, or a symmetrical layout.
