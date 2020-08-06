from sys import argv, exit
import csv
from cs50 import SQL

# Open database
db = SQL("sqlite:///students.db")

if len(argv) != 2:
    print("Usage Error: python roster.py house_name")
    exit(1)

housename = argv[1]
# rows is a list, each row is an individual element. Order first by last_name and then by first_name
rows = db.execute("SELECT first, middle, last, birth FROM students WHERE house=? ORDER BY last, first", housename)
# print out each row with their own line
for row in rows:
    if row['middle'] == None:
        print(f"{row['first']} {row['last']}, born {row['birth']}")
    else:
        print(f"{row['first']} {row['middle']} {row['last']}, born {row['birth']}")