import csv, urllib, requests

geocoded_addresses = {}

def geocode(address):
    if not geocoded_addresses.get(address):
        url = 'https://maps.googleapis.com/maps/api/geocode/json?'
        url += urllib.urlencode({'address': address})
        data = requests.get(url).json()
        row['lat'] = data['results'][0]['geometry']['location']['lat']
        row['lng'] = data['results'][0]['geometry']['location']['lng']
        geocoded_addresses[address] = (row['lat'], row['lng'])
    return geocoded_addresses[address]

with open("incidents.csv", "r") as fin, open('incidents_geocoded.csv', 'w') as fout:
    reader = csv.DictReader(fin)
    writer = csv.DictWriter(fout, fieldnames=reader.fieldnames + ['lat', 'lng'])
    writer.writeheader()
    for row in reader:
        address = row['Location'] + ". Evanston, IL 60201"
        row['lat'], row['lng'] = geocode(address)
        print row
        writer.writerow(row)

with open("tickets.csv", "r") as fin, open("tickets_geocoded.csv", "w") as fout:
    reader = csv.DictReader(fin)
    writer = csv.DictWriter(fout, fieldnames=reader.fieldnames + ['lat', 'lng'])
    writer.writeheader()
    for row in reader:
        address = row['Address of Occurrence'] + ". Evanston, IL 60201"
        row['lat'], row['lng'] = geocode(address)
        print row
        writer.writerow(row)