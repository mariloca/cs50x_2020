import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

#API_KEY=pk_b94486403d79464faadabbc3d003ec44
#message flashing
#https://flask.palletsprojects.com/en/1.1.x/patterns/flashing/

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    purchasedict = {}
    holdingdict = {}
    selldict = {}

    # Get stock and shares from 'purchase' table for current user
    stocklist = db.execute(
        "SELECT stock, SUM(share) as shares FROM purchase WHERE  user_id=:user_id GROUP BY stock", user_id=session['user_id'])
    # Keys:symbol, Values:shares
    for item in stocklist:
        purchasedict[item['stock']] = item['shares']

    # Get stock and shares from 'sell' table
    selllist = db.execute("SELECT stock, SUM(share) as shares FROM sell WHERE  user_id=:user_id GROUP BY stock",
                          user_id=session['user_id'])
    for item in selllist:
        selldict[item['stock']] = item['shares']

    # Calculate currently holding shares using ('purchase.shares' + 'sell.shares(negative)')
    for key in purchasedict:
        if key in selldict:
            purchasedict[key] = int(purchasedict[key]) + int(selldict[key])

    # Get stock and shares from 'marketvalue' table
    holdinglist = db.execute("SELECT stock, shares FROM marketvalue WHERE user_id=:user_id", user_id=session['user_id'])
    for item in holdinglist:
        holdingdict[item['stock']] = item['shares']

    # Check stock information
    for k in purchasedict:
        pricedict = lookup(k)
        price = float(pricedict['price'])  # Current stock price
        total = float(int(purchasedict[k]) * price)  # Current stock market value
        name = pricedict['name']  # Symbol company name

    # if purchasedict.keys in holdingdict, update shares in 'marketvalue'
        if k in holdingdict.keys():
            db.execute("UPDATE marketvalue SET shares=:shares, totalvalue=:totalvalue, price=:price WHERE user_id=:user_id AND stock=:stock",
                       shares=purchasedict[k], totalvalue=total, price=price, user_id=session['user_id'], stock=k)
    # if purchasedict.keys not in holdingdict, insert key and value as stock and shares into 'marketvalue'
        else:
            db.execute("INSERT or IGNORE INTO marketvalue (user_id, stock, shares, price, totalvalue, name, currentdate) VALUES (:user_id, :stock, :shares, :price, :totalvalue, :name, CURRENT_TIMESTAMP)",
                       user_id=session['user_id'], stock=k, shares=purchasedict[k], price=price, totalvalue=total, name=name)

    # If stock shares ==0: delete stock record in 'marketvalue'
    db.execute("DELETE FROM marketvalue WHERE user_id=:user_id AND shares=:shares", user_id=session['user_id'], shares=0)

    # Index.html table display
    balance = 0
    holdings = db.execute(
        "SELECT stock, name, shares, price, totalvalue FROM marketvalue WHERE user_id=:user_id GROUP BY stock", user_id=session["user_id"])
    for item in holdings:
        valuefloat = float(item['totalvalue'])
        balance += valuefloat
        item['price'] = usd(item['price'])
        item['totalvalue'] = usd(item['totalvalue'])

    cashdict = db.execute("SELECT cash FROM users WHERE id=:id", id=session['user_id'])
    cash = float(cashdict[0]['cash'])

    # balance is total of all current holding stock value
    balance = round(balance, 2)
    # totalbalance is balance + cash
    totalbalance = round((balance+cash), 2)
    return render_template("index.html", holdings=holdings, cashbalance=usd(cash), totalbalance=usd(totalbalance))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("purchase.html")
    else:
        symbol = request.form.get("symbol")
        # Ensure symbol is not blank
        if not symbol:
            return apology("Missing symbol")
        symbol = symbol.upper()
        quotedict = lookup(symbol)
        # Ensure symbol is valid
        if quotedict == None:
            return apology("Invalid symbol")
        else:
            # Calculate buying power for current stock
            price = quotedict['price']
            shares = request.form.get("shares")
            stocktotal = float(price) * int(shares)
            userid = session["user_id"]
            row = db.execute("SELECT cash FROM users WHERE id = :id", id=userid)
            balance = row[0]['cash']

            '''
            debug: print out variable in a new html page
            return render_template("buytest.html", balance=balance, money=stocktotal, user=session['user_id'])
            '''

            if balance > stocktotal:
                # Insert buying information into purchase table
                db.execute("INSERT INTO purchase (user_id, stock, share, price, value, currentdate) VALUES (:user_id, :stock, :share, :price, :value, CURRENT_TIMESTAMP)",
                           user_id=session["user_id"], stock=symbol, share=shares, price=price, value=stocktotal)
                db.execute("INSERT INTO history (user_id, stock, share, price, value, currentdate) VALUES (:user_id, :stock, :share, :price, :value, CURRENT_TIMESTAMP)",
                           user_id=session["user_id"], stock=symbol, share=shares, price=price, value=stocktotal)
                # Update cash information in users table
                currentbalance = float(balance) - stocktotal
                db.execute("UPDATE users SET cash=:cash WHERE id=:id", cash=currentbalance, id=userid)

                # Redirect user to home page
                flash('Bought!')
                return redirect("/")
            else:
                return apology("Not enough cash")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    holdings = db.execute("SELECT stock, share, price, currentdate FROM history WHERE user_id=:user_id", user_id=session["user_id"])
    for item in holdings:
        item['price'] = usd(item['price'])
    return render_template("history.html", holdings=holdings)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        flash('Logged in!')
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")

    else:
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Missing symbol")
        symbol = symbol.upper()
        # lookup function return a dict
        quotedict = lookup(symbol)

        # Ensure symbol is valid
        if quotedict == None:
            return apology("Invalid symbol")
        else:
            return render_template("quoted.html", company=quotedict['name'], symbol=quotedict['symbol'], price=usd(quotedict['price']))


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    else:
        username = request.form.get("username")
        # Ensure username is not blank
        if not username:
            message = "You must provide a username."
            return apology(message)

        # Ensure username is unique
        usernames = db.execute("SELECT username FROM users")
        for row in usernames:
            if username == row['username']:  # row is returned as key-value pairs
                message = "This username has been registered, try another username."
                return apology(message)

        password = request.form.get("password")
        # Ensure password is not blank
        if not password:
            message = "You must provide a password."
            return apology(message)

        confirmation = request.form.get("confirmation")
        # Ensure password confirmation matches with password
        if not confirmation or password != confirmation:
            message = "You must confirm your password."
            return apology(message)

        # Give the password a hash value to be stored in the database
        passhash = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=username, hash=passhash)

        # Get session['user_id'] for this registered user, redirect the user to index.html with logged in info.
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=username)
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        flash('Registered!')
        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    owndict = db.execute("SELECT * FROM marketvalue WHERE user_id=:user_id", user_id=session['user_id'])
    if request.method == "GET":
        return render_template("sell.html", owndict=owndict,)
    else:
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        # Ensure symbol is selected
        if not symbol:
            return apology("You must select stock to sell.")
        # Ensure shares is entered with positive number
        if not shares or int(shares) < 0:
            return apology("You must enter valid share numbers.")

        selldict = lookup(symbol)
        sellprice = selldict['price']

        for item in owndict:
            # Ensure the user own some shares of the stock
            if symbol == item['stock']:
                if int(item['shares']) == 0:
                    return apology("You don't have any shares of this stock")
                # Ensure entered shares is less than current owned shares
                elif int(shares) > int(item['shares']):
                    return apology("You don't have this many shares to sell, please enter again.")
                else:
                    newshares = int(item['shares'])-int(shares)
                    newtotalvalue = newshares * sellprice
                    sellvalue = int(shares) * sellprice
                    # Update 'user.cash'
                    cashdict = db.execute("SELECT cash FROM users WHERE id=:id", id=session['user_id'])
                    cash = float(cashdict[0]['cash']) + sellvalue
                    db.execute("UPDATE users SET cash=:cash WHERE id=:id", cash=cash, id=session['user_id'])
                    # Insert sell record into sell table
                    db.execute("INSERT or IGNORE INTO sell (user_id, stock, share, price, value, currentdate) VALUES (:user_id, :stock, :share, :price, :value, CURRENT_TIMESTAMP)",
                               user_id=session['user_id'], stock=symbol, share=("-" + shares), price=sellprice, value=sellvalue)
                    db.execute("INSERT INTO history (user_id, stock, share, price, value, currentdate) VALUES (:user_id, :stock, :share, :price, :value, CURRENT_TIMESTAMP)",
                               user_id=session["user_id"], stock=symbol, share=("-" + shares), price=sellprice, value=sellvalue)
        flash('Sold!')
        return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
