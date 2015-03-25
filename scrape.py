import requests, lxml.html
from calendar import month_abbr
from pprint import pprint as pp

from models import db, incidents, tickets

db.drop_collection("incidents")
db.drop_collection("tickets")

sections = ["Evanston Campus Incidents", "Compliants Tickets Issued"]

for i in range(2014,2015+1):
	for j in range(1,12+1):
		if i == 2014 and j < 3: continue # start from March 2014
		if i == 2015 and j > 2: break	 # stop at Febraruy 2015
		url = "http://www.northwestern.edu/up/blotter/blotter_ev-%s%d.html" % (month_abbr[j].lower(), i)
		response = requests.get(url)
		doc = lxml.html.fromstring(response.content)
		tables = [x for x in doc.cssselect("table") if len(x.getchildren()) > 1]

		blotters = []

		for table, section in zip(tables, sections):
			for blotter_first_row in table.cssselect("tr.blottercase"):
				row = blotter_first_row
				blotter = {}
				while True:
					key = row.cssselect("td:nth-child(1)")[0].text_content().replace(":", "")
					if key == "Date & Time Occurred":
						values = [
							row.cssselect("td:nth-child(2)")[0].text_content(),
							row.getnext().cssselect("td:nth-child(2)")[0].text_content()
						]
						blotter["Date & Time Occurred Start"] = values[0]
						blotter["Date & Time Occurred End"] = values[1]
						row = row.getnext().getnext()
					else:
						value = row.cssselect("td:nth-child(2)")[0].text_content().strip()
						if key != u'\xa0': blotter[key] = value
						row = row.getnext()
					if (row is None) or (row.get('class') and 'blottercase' in row.get('class')): break
				if section == "Evanston Campus Incidents":
					blotter['_id'] = blotter.pop('Case Number')
					incident = incidents.find_one({"_id": blotter['_id']})
					if incident:
						print incident
						incident['Criminal Offense'] += "\n" + blotter['Criminal Offense']
						incidents.save(incident)
					else:
						incidents.insert(blotter)
				elif section == "Compliants Tickets Issued":
					blotter['_id'] = blotter.pop('Ticket Number')
					tickets.insert(blotter)

				pp(blotter)
