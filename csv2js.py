import csv, json

data = []

with open("incidents_geocoded.csv", "rU") as f:
	reader = csv.DictReader(f)
	for row in reader: data.append(row)

json.dump(data, open("incidents_geocoded.js", "w"))