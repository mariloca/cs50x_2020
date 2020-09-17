# Finance Project - Create a Stock Trade website
Implement a website via which users can “buy” and “sell” stocks, a la the below.

## Overview
Implement Finance, a web app via which you can manage portfolios of stocks. Not only will this tool allow you to check real stocks’ actual prices and portfolios’ values, it will also let you buy (okay, “buy”) and sell (okay, “sell”) stocks by querying [IEX](https://iexcloud.io/) for stocks’ prices.

IEX lets you download stock quotes via their API (application programming interface) using URLs like https://cloud-sse.iexapis.com/stable/stock/nflx/quote?token=API_KEY. 

### Code Structure
- *static/: saves styles.css, which has some initial CSS lives
- templates/:
  - In login.html is, essentially, just an HTML form, stylized with Bootstrap In apology.html, meanwhile, is a template for an apology. Recall that apology in helpers.py took two arguments: message, which was passed to render_template as the value of bottom, and, optionally, code, which was passed to render_template as the value of top. Notice in apology.html how those values are ultimately used! And here’s why. 0:-)

Last up is layout.html. It’s a bit bigger than usual, but that’s mostly because it comes with a fancy, mobile-friendly “navbar” (navigation bar), also based on Bootstrap. Notice how it defines a block, main, inside of which templates (including apology.html and login.html) shall go. It also includes support for Flask’s message flashing so that you can relay messages from one route to another for the user to see.

- *are files have been written by cs50.

### Environment
Run on [CS50 IDE](https://ide.cs50.io/).
Log in with your github account.

### Configuration
In a terminal window within CS50 IDE, execute:
```
$ export API_KEY=pk_b94486403d79464faadabbc3d003ec44
```

### Running
Start Flask's built-in web server:
```
$ flask run
```
Visit the URL outputted by flask.



CS50 Finance project link:[CS50 Finance](https://cs50.harvard.edu/x/2020/tracks/web/finance/)






