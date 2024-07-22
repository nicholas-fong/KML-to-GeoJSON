# Convert GeoJSON Point, LineString, Polygon object to KML Point, LineString, Polygon placemarks
# Convert GeoJSON MultiPoint to KML MultiGeometry Point
# Convert GeoJSON MultiLineString to KML MultiGeometry LineString
# Convert GeoJSON MultipPolygon to KML MultiGeometry Polygon
# Convert GeoJSON GeometryCollection Point, LineString and Polygon to KML MultiGeometry placemarks
# or use https://geojson.io

import json
import sys
from lxml import etree as ET     # pip install lxml
import xml.dom.minidom as minidom

# Load GeoJSON data
try:
    with open(sys.argv[1]+'.geojson', 'r') as infile:
        data = json.load(infile)
except FileNotFoundError:
    print(f"Error: File {sys.argv[1]}.geojson not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print("Error: Failed to parse GeoJSON file.")
    sys.exit(1)

# Create a KML root element
kml = ET.Element('kml', xmlns='http://www.opengis.net/kml/2.2')

# Create a KML document element
document = ET.SubElement(kml, 'Document')

# A function to convert GeoJSON feature to KML placemark
def geojson_feature_to_kml(feature):
    placemark = ET.SubElement(document, 'Placemark')

    property = feature.get('properties', None)
    if property is not None:
        # Extract the name
        name = feature['properties'].get('name', '') or feature['properties'].get('NAME', '') or feature['properties'].get('Name', '')
        if name:
            name_element = ET.SubElement(placemark, 'name')
            name_element.text = name
        # Extract properties description
        description = feature['properties'].get('description', None)
        if description:
            desc_element = ET.SubElement(placemark, 'description')
            desc_element.text = description
        # Extract timestamp
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
    if  feature['geometry']['type'] == 'MultiPoint':
        multigeometry = ET.SubElement(placemark, 'MultiGeometry')
        for each_coords in feature['geometry']['coordinates']:
            point = ET.SubElement(multigeometry, 'Point')
            coordinates = ET.SubElement(point, 'coordinates')
            coordinates.text = ','.join(map(str, each_coords))
    if feature['geometry']['type'] == 'LineString':
        linestring = ET.SubElement(placemark, 'LineString')
        coordinates = ET.SubElement(linestring, 'coordinates')
        coordinates.text = ' '.join(','.join(map(str, coords)) for coords in feature['geometry']['coordinates'])
    if feature['geometry']['type'] == 'MultiLineString':
        multigeometry = ET.SubElement(placemark, 'MultiGeometry')
        for each_line in feature['geometry']['coordinates']:
            linestring = ET.SubElement(multigeometry, 'LineString')
            coordinates = ET.SubElement(linestring, 'coordinates')
            coordinates.text = ' '.join(','.join(map(str, coords)) for coords in each_line)
    if feature['geometry']['type'] == 'Polygon':
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
    if feature['geometry']['type'] == 'MultiPolygon':
        multigeometry = ET.SubElement(placemark, 'MultiGeometry')
        for item in feature['geometry']['coordinates']:
            polygon = ET.SubElement(multigeometry, 'Polygon')
            outer = ET.SubElement(polygon, 'outerBoundaryIs')
            linear_ring = ET.SubElement(outer, 'LinearRing')
            coordinates = ET.SubElement(linear_ring, 'coordinates')
            coordinates.text = ' '.join(','.join(map(str, coords)) for coords in item[0] )
            for inner_ring_coords in item[1:]:
                inner = ET.SubElement(polygon, 'innerBoundaryIs')
                inner_ring = ET.SubElement(inner, 'LinearRing')
                inner_coordinates = ET.SubElement(inner_ring, 'coordinates')
                inner_coordinates.text = ' '.join(','.join(map(str, coords)) for coords in inner_ring_coords)
    if feature['geometry']['type'] == 'GeometryCollection':
        multi= ET.SubElement(placemark, 'MultiGeometry')            
        for item in feature['geometry']['geometries']:
            if item['type']=='Point':
                point = ET.SubElement(multi, 'Point')
                coordinates = ET.SubElement(point, 'coordinates')
                coordinates.text = ','.join(map(str, item['coordinates']))
            if item['type']=='LineString':
                linestring = ET.SubElement(multi, 'LineString')
                coordinates = ET.SubElement(linestring, 'coordinates')
                coordinates.text = ' '.join(','.join(map(str, coords)) for coords in item['coordinates']) 
            if item['type']=='Polygon':
                polygon = ET.SubElement(multi, 'Polygon')
                outer = ET.SubElement(polygon, 'outerBoundaryIs')
                linear_ring = ET.SubElement(outer, 'LinearRing')
                coordinates = ET.SubElement(linear_ring, 'coordinates')
                coordinates.text = ' '.join(','.join(map(str, coords)) for coords in item['coordinates'][0])
                for inner_ring_coords in item['coordinates'][1:]:
                    inner = ET.SubElement(polygon, 'innerBoundaryIs')
                    inner_ring = ET.SubElement(inner, 'LinearRing')
                    inner_coordinates = ET.SubElement(inner_ring, 'coordinates')
                    inner_coordinates.text = ' '.join(','.join(map(str, coords)) for coords in inner_ring_coords)

# style 1 of pretty print, eliminat blank lines, returns regular string
def prettify(element):
    rough_string = ET.tostring(element, encoding='utf-8', xml_declaration=True)
    reparsed = minidom.parseString(rough_string)
    pretty_string = (reparsed.toprettyxml(indent="  ", encoding='utf-8')).decode('utf-8')
    # Remove extra blank lines
    lines = [line for line in pretty_string.split('\n') if line.strip()]
    return '\n'.join(lines)
# style 2 of pretty print: ET.tosring --> minidom --> toprettyxml, returns binary string
# def prettify(element):
#   rough_string = ET.tostring(element, encoding='utf-8', xml_declaration=True)
#   reparsed = minidom.parseString(rough_string)
#   return reparsed.toprettyxml(indent="  ", encoding='utf-8')
# style 3 KML to string pretty print
# print( ET.tostring(kml, encoding='utf-8', pretty_print=True, xml_declaration=True ).decode() )

# main()
# Iterate through GeoJSON features and create KML placemark for each feature
for feature in data['features']:
    geojson_feature_to_kml(feature)

# sylte 1 output: <?xml version="1.0" encoding="utf-8"?>
pretty_kml = prettify(kml)
#print (pretty_kml)
with open(sys.argv[1]+'.kml', 'w') as output_file:
    output_file.write(pretty_kml)
print ( f"File saved as {sys.argv[1]+'.kml'}")    
# style 2 output: <?xml version='1.0' encoding='UTF-8'?>
# super simple, but uses '' instead of ""
# tree.write(sys.argv[1] + ".kml", encoding="utf-8", xml_declaration=True)
