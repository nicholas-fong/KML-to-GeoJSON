# input a CSV (asc) file and create corresponding GeoJSON file.
# CSV (asc) file has 3 columns, latitude, longitude and name of the geo location (Point)
# the third column (name field) can be quoted or unquoted
# create a .geojson file
# assume CSV data is WGS84 latitude and longitude
# quotation marks in third column (name field) are optional and are filtered out, but don't use comma in this field.
# leading and trailing blanks in name filed are also filtered out
# additional columns beyond column 3 are ignored
# Note: no elevation data, they are default to 0 

import sys
import csv
import json
from geojson import FeatureCollection, Feature, Point

if len(sys.argv) < 2:
    print("Please enter a CSV file. File extension .asc is assumed") 
    sys.exit(1)

basket = []             # empty basket to hold/collect features

with open(sys.argv[1]+'.asc') as infile:
    reader = csv.reader(infile, delimiter=',')
    for row in reader:
        if row:         #extra if statement to capture empty lines
            my_name=row[2].replace('"', '').strip()
            lat = float(row[0])
            lon = float(row[1])
            elev = 0.0    
            my_point=Point([lon,lat,elev])
            basket.append(Feature(geometry=my_point, properties={"name":my_name}))

geo_string = json.dumps( FeatureCollection(basket), indent=2, ensure_ascii=False )

with open(sys.argv[1]+'.geojson', 'w') as outfile:
    outfile.write( geo_string )

print(geo_string)
