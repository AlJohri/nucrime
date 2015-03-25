import csv, json

incidents_data = []

with open("incidents_geocoded.csv", "rU") as f:
	reader = csv.DictReader(f)
	for row in reader: incidents_data.append(row)

json.dump(incidents_data, open("incidents.js", "w"))

tickets_data = []

with open("tickets_geocoded.csv", "rU") as f:
	reader = csv.DictReader(f)
	for row in reader: tickets_data.append(row)

json.dump(tickets_data, open("tickets.js", "w"))