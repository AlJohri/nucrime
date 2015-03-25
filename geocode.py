import csv, urllib, requests

geocoded_addresses = {}

with open("incidents.csv", "r") as fin, open('incidents_geocoded.csv', 'w') as fout:
    reader = csv.DictReader(fin)
    writer = csv.DictWriter(fout, fieldnames=reader.fieldnames + ['lat', 'lng'])
    writer.writeheader()
    for row in reader:
        address = row['Location'] + ". Evanston, IL 60201"
        if geocoded_addresses.get(address):
            row['lat'], row['lng'] = geocoded_addresses[address]
        else:
            url = 'https://maps.googleapis.com/maps/api/geocode/json?'
            url += urllib.urlencode({'address': address})
            data = requests.get(url).json()
            row['lat'] = data['results'][0]['geometry']['location']['lat']
            row['lng'] = data['results'][0]['geometry']['location']['lng']
            geocoded_addresses[address] = (row['lat'], row['lng'])
        print row
        writer.writerow(row)