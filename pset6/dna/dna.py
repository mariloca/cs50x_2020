from sys import argv, exit
import csv


def main():
    # Read text file into memory
    file = open(argv[2])
    sequence = file.read()  # Type string
    # Check command-line argument
    if len(argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        exit(1)

    # Read csv file into memory
    tmplist = []
    flag = 0
    with open(argv[1], newline='') as csvfile:
        database = csv.reader(csvfile)
        strlist = next(database)  # list of all STRs
        sequencedict = computecount(strlist, sequence)
        # print("s:", sequencedict)
        for row in database:
            tmplist = row  # stores row of the csv file
            comparedict = makedict(strlist, tmplist)
            # Compare STRs counts against each row in csv file
            if sequencedict == comparedict:
                print(tmplist[0])
                flag = 1

    if flag == 0:
        print("No match")

# Compute longest run of consecutive repeats in DNA, passing dnalist and sequence


def computecount(alist, astring):
    dnadict = dict()
    for i in range(1, len(alist)):
        j = 0
        count = 0
        countmax = 0
        n = len(alist[i])
        while j < len(astring):
            if astring[j:j+n] == alist[i]:
                count += 1
                j += n  # move to next sub-string
                if count > countmax:
                    countmax = count
            else:
                count = 0
                j += 1  # move to next char
            dnadict[alist[i]] = countmax
    return dnadict

# passing dnalist, row list


def makedict(alist, blist):
    i = 0
    comparedict = dict()
    for i in range(1, len(alist)):
        comparedict[alist[i]] = int(blist[i])
    return comparedict

if __name__ == "__main__":
    main()
