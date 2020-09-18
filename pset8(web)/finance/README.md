# Finance Project - Create a Stock Trade website
Implement a website via which users can “buy” and “sell” stocks, a la the below.

## Overview
Implement Finance, a web app via which you can manage portfolios of stocks. Not only will this tool allow you to check real stocks’ actual prices and portfolios’ values, it will also let you buy (okay, “buy”) and sell (okay, “sell”) stocks by querying [IEX](https://iexcloud.io/) for stocks’ prices.

IEX lets you download stock quotes via their API (application programming interface) using URLs like https://cloud-sse.iexapis.com/stable/stock/nflx/quote?token=API_KEY. 

### Code Structure
- static/: saves styles.css, which has some initial CSS lives
- templates/: template for each webpages
- helpers.py: has 4 helper functions used in application.py
- application.py: implements 8 routes of the web App
- finance.db: database that stores user information and stock trading records
- requirements.txt: prescribes the packages on which this app will depend

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



CS50 Finance project link: [CS50 Finance](https://cs50.harvard.edu/x/2020/tracks/web/finance/)






