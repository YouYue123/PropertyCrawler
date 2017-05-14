import json
import csv
dict = {}
result = []

with open('distance1.json') as data_file:
    data = json.load(data_file)
    for item in data:
        postcode = int(item['url'][95:])
        if postcode > 0:
            distance = item['distance']
            dict[postcode] = distance

with open('postcode.csv', 'rU') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        postcode = int(row[1])
        address = row[0]
        distance = '-1 km'
        if postcode != 0:
            distance = dict[postcode]
        item = []
        item.append(address)
        item.append(postcode)
        item.append(distance)
        result.append(item)
with open('distance2.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for row in result:
        print row
        writer.writerow([row[0],row[1],row[2]])
