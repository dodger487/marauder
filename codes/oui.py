import csv

codes = []

with open("oui.txt") as f:
    with open('codes.csv', 'wb') as csvfile:
        codewriter = csv.writer(csvfile)
        for line in f:
            if len(line) > 4 and line[4] == "-":
                codewriter.writerow([line[2:10].lower().replace("-", ":"), line[20:-1]])
