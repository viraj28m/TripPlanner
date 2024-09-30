import csv

def removeCommaSpace(s):
    loc = s.find(", ")
    if loc != -1:
        return s[loc + 2:] + " " + s[:loc]
    return s

lines = []

with open('static/data/worldcities.csv') as f:
    csvFile = csv.reader(f)
    for line in csvFile:
        lines.append(line)


# City (unicode), City (ascii), lat, lng, country, iso2, iso3, admin_name (optional), ...
#       0              1          2    3     4       5     6        7     

lines = lines[1:10000]

allCities = []
for line in lines:
    city = removeCommaSpace(line[1])
    country = removeCommaSpace(line[4])
    admin_name = removeCommaSpace(line[7])
    if admin_name:
        allCities.append(city + ", " + admin_name + ", " + country)
    else:
        allCities.append(city + ", " + country)

print(allCities)

