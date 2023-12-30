# input a CSV (ascii) file and create corresponding GeoJSON file.
# CSV (asc) file has 3 columns, latitude, longitude and name of the geo location (Point)
# the third column (name field) can be quoted or unquoted
# create a .geojson file
# assume CSV data is WGS84 latitude and longitude
# quotation marks in third column (name field) are optional and are filtered out, but don't use comma in this field.
# leading and trailing blanks in name filed are also filtered out
# additional columns beyond column 3 are ignored
# Note: no elevation data, they are default to 0 

import csv
import sys
import json

# Input and output file paths
input_file_path = sys.argv[1] + '.asc'
output_file_path = sys.argv[1] + '.geojson'

# Read data from the ASCII file
features = []
with open(input_file_path) as infile:
    reader = csv.reader(infile, delimiter=',')
    for row in reader:
        if row:
            lat = float(row[0])
            lon = float(row[1])
            elev = 0
            my_name = row[2].replace('"', '').strip()

            # Create a GeoJSON Point feature
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat, elev]
                },
                "properties": {
                    "name": my_name
                }
            }

            features.append(feature)

# Create a GeoJSON FeatureCollection
geojson_data = {
    "type": "FeatureCollection",
    "features": features
}

# Write GeoJSON data to a file
with open(output_file_path, 'w') as outfile:
    json.dump(geojson_data, outfile, indent=2)

#print(json.dumps(eval("geojson_data"), indent=2))
