from sys import argv, exit
import csv
from cs50 import SQL

open(f"students.db", "w").close()
# Create a new database
db = SQL("sqlite:///students.db")
# Create a new table
db.execute("CREATE TABLE students (first TEXT, middle TEXT, last TEXT, house TEXT, birth NUMERIC)")

file = open(argv[1])
rfile = file.read()
if len(argv) != 2:
    print("Usage Error: python import.py characters.csv")
    exit(1)

# Open and read csv file
with open(argv[1], "r") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    # Each row in reader is like OrderedDict([('name', 'Adelaide Murton'), ('house', 'Slytherin'), ('birth', '1982')])
    for row in reader:
        # row['name']is a string, so split it into a list to get each name
        namelist = row['name'].split()
        if len(namelist) == 2:
            f = namelist[0]
            l = namelist[1]
            m = None
        if len(namelist) == 3:
            f = namelist[0]
            m = namelist[1]
            l = namelist[2]

        db.execute("INSERT INTO students(first, middle, last, house, birth) VALUES(?,?,?,?,?)", f, m, l, row['house'], row['birth'])
