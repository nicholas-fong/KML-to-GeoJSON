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

            # Create a GeoJSON feature
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
