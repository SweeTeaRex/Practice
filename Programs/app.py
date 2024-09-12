import os
from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, usd

# Configure application
app = Flask(__name__)
app.secret_key = 'key'

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_SAMESITE"] = "None"  # Set SameSite to None
app.config["SESSION_COOKIE_SECURE"] = True

Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///blackjack.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



@app.route("/")
def index():
    user_id = session.get('user_id')
    
    logged_in = False
    
    if user_id:
        # Check if the user exists in the database
        user_exists = db.execute('SELECT id FROM players WHERE id = ?', (user_id,))
        
        if user_exists:
            logged_in = True

    return render_template("index.html", user_id=user_id, logged_in=logged_in)


@app.route('/check_login', methods=['POST'])
def check_login():
    user_id = session.get('user_id', None)
    response = {"logged_in": False, "user_id": user_id or ''}
    
    if user_id:        
        cursor = db.execute('SELECT id FROM players WHERE id = ?', (user_id,))
        user_exists = cursor.fetchone()      
        if user_exists:
            response = {"logged_in": True}
    
    return response
    
       
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    user_id = session.get('user_id', None)
    
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM players WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["password"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/playerpage")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html", user_id=user_id)
    
@app.route('/casino')
@login_required

def casino():
    user_id = session.get('user_id', None)
    
    return render_template('casino.html', user_id=user_id)

@app.route("/register", methods=["GET", "POST"])

def register():
    user_id = session.get('user_id', None)
    """Register user"""
    if request.method == "GET":

        return render_template("register.html", user_id=user_id)
    elif request.method == "POST":
        #first name
        firstname = request.form.get("firstname")

        if not firstname:
            return apology("Need vaild first name")
        #username
        username1 = request.form.get("username")

        #no blank space
        username = username1.strip()

        #404 if nothing
        if not username:
            return apology("Need vaild username")

        #get username from db
        checkUsername = db.execute('SELECT username FROM players WHERE username = ?', username)

        #if username exists, return apology
        if len(checkUsername) > 0:
            return apology("Username already exists", 400)
        #password
        password = request.form.get("password")

        if not password:
            return apology("Need Password", 400)
        #pw confirmation
        passwordC = request.form.get("confirmation")

        if not passwordC:
            return apology("Need Password", 400)

        if passwordC != password:
            return apology("Passwords do not match", 400)

        pwhash = generate_password_hash(password)

        newUserInput = db.execute("INSERT INTO players (username, password, name) VALUES (?, ?, ?);", username, pwhash, firstname)

        return redirect("/")

@app.route('/howtoplay')

def howtoplay():
    user_id = session.get('user_id', None)
    return render_template('howtoplay.html', user_id=user_id)


@app.route('/playerpage')
@login_required
def playerpage():
    user_id = session.get('user_id')
    name1 = db.execute("SELECT name FROM players WHERE id = ?", user_id)
    name = name1[0]['name']
    bank1 = db.execute("SELECT cash FROM players WHERE id =?", user_id)
    bank = usd(bank1[0]['cash'])
    return render_template('playerpage.html', name=name, user_id=user_id, bank=bank)


@app.route('/logout')

def logout():
    session.clear()
    return redirect(url_for('index'))






if __name__ == '__main__':
    app.run(debug=True)