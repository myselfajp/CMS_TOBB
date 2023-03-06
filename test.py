import csv

import csv
rows = []
with open("AZERBEYCAN.csv", 'r') as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    for row in csvreader:
        print(row)
        rows.append(row)
