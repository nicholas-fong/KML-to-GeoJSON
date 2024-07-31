import json
import sys
from lxml import etree as ET     # pip install lxml
import xml.dom.minidom as minidom

NAMESPACE = 'http://www.opengis.net/kml/2.2'

# Load GeoJSON data
try:
    with open(sys.argv[1] + '.geojson', 'r') as infile:
        data = json.load(infile)
except FileNotFoundError:
    print(f"Error: File {sys.argv[1]}.geojson not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print("Error: Failed to parse GeoJSON file.")
    sys.exit(1)

# Create a KML root element and document folder
kml = ET.Element('kml', xmlns=NAMESPACE)
document = ET.SubElement(kml, 'Document')

def prettify(element):
    rough_string = ET.tostring(element, encoding='utf-8', xml_declaration=True)
    reparsed = minidom.parseString(rough_string)
    pretty_string = (reparsed.toprettyxml(indent="  ", encoding='utf-8')).decode('utf-8')
    return '\n'.join(line for line in pretty_string.split('\n') if line.strip())

def add_property_element(placemark, tag, value):
    if value:
        element = ET.SubElement(placemark, tag)
        element.text = value

def add_coordinates_element(parent, coords):
    coordinates = ET.SubElement(parent, 'coordinates')
    coordinates.text = ' '.join(','.join(map(str, coord)) for coord in coords)

def handle_point(parent, coords):
    point = ET.SubElement(parent, 'Point')
    add_coordinates_element(point, [coords])

def handle_multi_point(parent, coords_list):
    multigeometry = ET.SubElement(parent, 'MultiGeometry')
    for coords in coords_list:
        point = ET.SubElement(multigeometry, 'Point')
        add_coordinates_element(point, [coords])

def handle_line_string(parent, coords):
    linestring = ET.SubElement(parent, 'LineString')
    add_coordinates_element(linestring, coords)

def handle_multi_line_string(parent, coords_list):
    multigeometry = ET.SubElement(parent, 'MultiGeometry')
    for coords in coords_list:
        linestring = ET.SubElement(multigeometry, 'LineString')
        add_coordinates_element(linestring, coords)

def handle_polygon(parent, coords_list):
    polygon = ET.SubElement(parent, 'Polygon')
    outer = ET.SubElement(polygon, 'outerBoundaryIs')
    linear_ring = ET.SubElement(outer, 'LinearRing')
    add_coordinates_element(linear_ring, coords_list[0])
    for inner_ring_coords in coords_list[1:]:
        inner = ET.SubElement(polygon, 'innerBoundaryIs')
        inner_ring = ET.SubElement(inner, 'LinearRing')
        add_coordinates_element(inner_ring, inner_ring_coords)

def handle_multi_polygon(parent, coords_list):
    multigeometry = ET.SubElement(parent, 'MultiGeometry')
    for polygon_coords in coords_list:
        polygon = ET.SubElement(multigeometry, 'Polygon')
        outer = ET.SubElement(polygon, 'outerBoundaryIs')
        linear_ring = ET.SubElement(outer, 'LinearRing')
        add_coordinates_element(linear_ring, polygon_coords[0])
        for inner_ring_coords in polygon_coords[1:]:
            inner = ET.SubElement(polygon, 'innerBoundaryIs')
            inner_ring = ET.SubElement(inner, 'LinearRing')
            add_coordinates_element(inner_ring, inner_ring_coords)

def handle_geometry_collection(parent, geometries):
    multigeometry = ET.SubElement(parent, 'MultiGeometry')
    for geometry in geometries:
        geo_type = geometry['type']
        coords = geometry['coordinates']
        if geo_type == 'Point':
            handle_point(multigeometry, coords)
        elif geo_type == 'LineString':
            handle_line_string(multigeometry, coords)
        elif geo_type == 'Polygon':
            handle_polygon(multigeometry, coords)

def geojson_feature_to_kml(feature):
    placemark = ET.SubElement(document, 'Placemark')
    properties = feature.get('properties', {})
    
    add_property_element(placemark, 'name', properties.get('name') or properties.get('NAME') or properties.get('Name'))
    add_property_element(placemark, 'description', properties.get('description'))
    timestamp = properties.get('timestamp') or properties.get('TimeStamp')
    if timestamp:
        timestamp_element = ET.SubElement(placemark, 'TimeStamp')
        when_element = ET.SubElement(timestamp_element, 'when')
        when_element.text = timestamp
    
    geometry = feature['geometry']
    geo_type = geometry['type']
    
    if geo_type == 'Point':
        handle_point(placemark, geometry['coordinates'])
    elif geo_type == 'MultiPoint':
        handle_multi_point(placemark, geometry['coordinates'])
    elif geo_type == 'LineString':
        handle_line_string(placemark, geometry['coordinates'])
    elif geo_type == 'MultiLineString':
        handle_multi_line_string(placemark, geometry['coordinates'])
    elif geo_type == 'Polygon':
        handle_polygon(placemark, geometry['coordinates'])
    elif geo_type == 'MultiPolygon':
        handle_multi_polygon(placemark, geometry['coordinates'])
    elif geo_type == 'GeometryCollection':
        handle_geometry_collection(placemark, geometry['geometries'])

# Main conversion
for feature in data.get('features', []):
    geojson_feature_to_kml(feature)

# Output the KML file
pretty_kml = prettify(kml)
output_file_path = sys.argv[1] + '.kml'
with open(output_file_path, 'w') as outfile:
    outfile.write(pretty_kml)
print(f"File saved as {output_file_path}")
