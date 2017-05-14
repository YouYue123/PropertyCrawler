import csv
import os

cwd = os.getcwd()
with open(cwd + '/postcode.csv', 'rU') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        print row[1]
