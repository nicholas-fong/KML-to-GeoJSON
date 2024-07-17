import sys
import json
import re
from geojson import FeatureCollection, Feature

# remove newlines and blanks in the coordinates array, for better readibility of the GeoJSON pretty print
def custom_dumps(obj, **kwargs):
    def compact_coordinates(match):
        # Remove newlines and extra spaces within the coordinates array
        return match.group(0).replace('\n', '').replace(' ', '')

    json_str = json.dumps(obj, **kwargs)
    # Use a more robust regex to match coordinate arrays
    json_str = re.sub(r'\[\s*([^\[\]]+?)\s*\]', compact_coordinates, json_str)
    return json_str

try:
    with open(sys.argv[1] + '.geojson', 'r', encoding='utf-8') as infile:
        data = json.load(infile)
except FileNotFoundError:
    print("file not found")
    sys.exit(1)
except json.JSONDecodeError:
    print("Error: Failed to parse GeoJSON file.")
    sys.exit(1)        

bucket = []
for feature in data['features']:
    bucket.append(Feature(geometry=feature['geometry'], properties=feature['properties']))

output_string = custom_dumps(FeatureCollection(bucket), indent=2, ensure_ascii=False)
#print(output_string)

with open(sys.argv[1] + '.geojson', 'w', encoding='utf-8') as outfile:
    outfile.write(output_string)

