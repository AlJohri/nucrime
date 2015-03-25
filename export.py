import csv
from models import incidents, tickets

incidents_fieldnames = ["_id", "Incident Type", "Date & Time Occurred Start", "Date & Time Occurred End", "Criminal Offense", "Date & Time Reported", "Location", "Common Name", "Disposition"]
tickets_fieldnames = ["_id", "Statute", "Address of Occurrence", "Ticket Date and Time", "Description"]

with open("incidents.csv", "w") as f:
	writer = csv.DictWriter(f, fieldnames=incidents_fieldnames)
	writer.writeheader()
	writer.writerows([incident for incident in incidents.find()])

with open("tickets.csv", "w") as f:
	writer = csv.DictWriter(f, fieldnames=tickets_fieldnames)
	writer.writeheader()
	writer.writerows([ticket for ticket in tickets.find()])
