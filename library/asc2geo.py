# input a CSV (asc) file and create corresponding GeoJSON file.
# CSV (asc) file has 3 columns: latitude, longitude and name of the geo location (Point)
# the third column (name field) can be quoted or unquoted
# output a geojson file
# assume CSV data is WGS84 latitude and longitude
# quotation marks in third column (name field) are optional and are filtered out, but don't use comma in this field.
# leading and trailing blanks in name filed are filtered out
# additional columns beyond column 3 are ignored
# elevation data are default to 0 in the geojson file

import sys
import re
import csv
import json
from geojson import FeatureCollection, Feature, Point

# remove newlines and blanks in the coordinates array, for better readibility of the GeoJSON pretty print
def custom_dumps(obj, **kwargs):
    def compact_coordinates(match):
        # Remove newlines and extra spaces within the coordinates array
        return match.group(0).replace('\n', '').replace(' ', '')

    json_str = json.dumps(obj, **kwargs)
    # Use a more robust regex to match coordinate arrays
    json_str = re.sub(r'\[\s*([^\[\]]+?)\s*\]', compact_coordinates, json_str)
    return json_str

if len(sys.argv) < 2:
    print("Please enter a CSV file. File extension .asc is assumed") 
    sys.exit(1)

basket = []             # empty basket to hold/collect features

try:
    with open(sys.argv[1]+'.asc') as infile:
        reader = csv.reader(infile, delimiter=',')
        for row in reader:
            if row:
                my_name=row[2].replace('"', '').strip()
                lat = float(row[0])
                lon = float(row[1])
                elev = 0.0    
                my_point=Point([lon,lat,elev])
                basket.append(Feature(geometry=my_point, properties={"name":my_name}))
except FileNotFoundError:
    print("file not found")
    sys.exit(1)                

geo_string = custom_dumps( FeatureCollection(basket), indent=2, ensure_ascii=False )

with open(sys.argv[1]+'.geojson', 'w') as outfile:
    outfile.write( geo_string )

