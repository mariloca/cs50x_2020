import re

text = input("Text:")
# split the text using [.!?] into a list, last element is " " (\0)
scount = len(re.split(r'[.!?]+', text))-1
# split the text use space into a list
wcount = len(re.split(r'[" "]+', text))
# Regular expression to find all alpha characters
lcount = len("".join(re.findall(r'[A-Z0-9a-z]', text)))
index = round(0.0588 * ((lcount * 100) / wcount) - 0.296 * ((scount * 100) / wcount) - 15.8)
if index < 1:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
else:
    print(f"Grade {index}")

