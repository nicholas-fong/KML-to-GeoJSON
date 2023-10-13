import json
import sys
import xml.etree.ElementTree as ET
import xml.dom.minidom

# Load your GeoJSON data from a file
with open( sys.argv[1]+'.geojson', 'r') as infile:
   geojson_data = json.load ( infile )

# Create a KML root element
kml = ET.Element('kml', xmlns='http://www.opengis.net/kml/2.2')

# Function to convert GeoJSON features to KML
def geojson_feature_to_kml(feature):
    placemark = ET.SubElement(kml, 'Placemark')

    yes_property = feature.get('properties', None)
    if yes_property:
        # Extract the name property
        name = feature['properties'].get('name', '')
        if name:
            name_element = ET.SubElement(placemark, 'name')
            name_element.text = name

        # Extract the timestamp in properties field if it exists
        timestamp = feature['properties'].get('timestamp', None)
        if timestamp is None:
            timestamp = feature['properties'].get('TimeStamp', None)
        if timestamp:
            timestamp_element = ET.SubElement(placemark, 'TimeStamp')
            when_element = ET.SubElement(timestamp_element, 'when')
            when_element.text = timestamp

    if feature['geometry']['type'] == 'Point':
        point = ET.SubElement(placemark, 'Point')
        coordinates = ET.SubElement(point, 'coordinates')
        coordinates.text = ','.join(map(str, feature['geometry']['coordinates']))
    elif feature['geometry']['type'] == 'LineString':
        linestring = ET.SubElement(placemark, 'LineString')
        coordinates = ET.SubElement(linestring, 'coordinates')
        coordinates.text = ' '.join(','.join(map(str, coords)) for coords in feature['geometry']['coordinates'])
    elif feature['geometry']['type'] == 'Polygon':
        polygon = ET.SubElement(placemark, 'Polygon')
        outer = ET.SubElement(polygon, 'outerBoundaryIs')
        linear_ring = ET.SubElement(outer, 'LinearRing')
        coordinates = ET.SubElement(linear_ring, 'coordinates')
        coordinates.text = ' '.join(','.join(map(str, coords)) for coords in feature['geometry']['coordinates'][0])
        
        for inner_ring_coords in feature['geometry']['coordinates'][1:]:
            inner = ET.SubElement(polygon, 'innerBoundaryIs')
            inner_ring = ET.SubElement(inner, 'LinearRing')
            inner_coordinates = ET.SubElement(inner_ring, 'coordinates')
            inner_coordinates.text = ' '.join(','.join(map(str, coords)) for coords in inner_ring_coords)

# Convert each GeoJSON feature to KML
for feature in geojson_data['features']:
    geojson_feature_to_kml(feature)

# Get the KML tree as a string
kml_string = ET.tostring(kml, encoding='utf-8')

# Pretty print the XML with 2-space indentation
kml_pretty = xml.dom.minidom.parseString(kml_string).toprettyxml(indent='  ')

# Print the prettified KML on the console
print(kml_pretty)

# Save the prettified KML to a file
with open(sys.argv[1]+'.kml', 'w') as output_file:
    output_file.write(kml_pretty)
