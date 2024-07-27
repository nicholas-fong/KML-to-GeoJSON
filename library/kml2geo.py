# Convert KML Point, LineString, Polygon and MultiGeometry
# to  GeoJSON Point, LineString, Polygon and GeometryCollection
# Convert KML gx:Track to GeoJSON LineString
# or install gdal-bin:  ogr2ogr outfile.geojson infile.kml

import sys
import xml.etree.ElementTree as ET
from geojson import FeatureCollection, Feature, Point, LineString, Polygon, GeometryCollection
import json
import re

kml_namespace = {'kml': 'http://www.opengis.net/kml/2.2'} 
gx_namespace =  {'gx': 'http://www.google.com/kml/ext/2.2'}

bucket=[]

# function to extract coordinates from a kml geometry element and returns a list of tuples
def extract_coordinates(geometry_element):
    coordinates_elem = geometry_element.find('kml:coordinates', kml_namespace)
    if coordinates_elem is not None:
        # coordinates is a list of strings
        coordinates = coordinates_elem.text.strip().split()
        # convert to a list of tuples
        list_of_tuples = [tuple(map(float, item.split(','))) for item in coordinates]
        return list_of_tuples

def pretty_dumps(obj, **kwargs):
    def compact_coordinates(match):
        # Remove newlines and extra spaces within the coordinates array
        return match.group(0).replace('\n', '').replace(' ', '')
    json_str = json.dumps(obj, **kwargs)
    # Use a more robust regex to match coordinate arrays
    json_str = re.sub(r'\[\s*([^\[\]]+?)\s*\]', compact_coordinates, json_str)
    return json_str

try:
    with open(sys.argv[1]+".kml") as infile:
        tree = ET.parse(infile)
    root = tree.getroot()
except FileNotFoundError:
    print(f"Error: File {sys.argv[1]}.kml not found.")
    sys.exit(1)
except ET.ParseError:
    print("Error: Failed to parse the KML file.")
    sys.exit(1)

root = tree.getroot()

# Find all placemark elements
for placemark in root.findall('.//kml:Placemark', kml_namespace):
    name_elem = placemark.find('.kml:name', kml_namespace)
    name = name_elem.text.strip() if name_elem is not None else 'Unnamed'
    time_elem = placemark.find('.kml:TimeStamp/kml:when', kml_namespace)
    time_stamp = time_elem.text.strip() if time_elem is not None else None

    point = placemark.find('.kml:Point', kml_namespace)
    line_string = placemark.find('.kml:LineString', kml_namespace)
    polygon = placemark.find('.kml:Polygon', kml_namespace)
    multigeometry = placemark.find('.kml:MultiGeometry', kml_namespace)
    gx_track = placemark.find('gx:Track', gx_namespace)

    if point is not None:
        geo_point = extract_coordinates(point)
        bucket.append(Feature(geometry=Point(geo_point[0]), properties={"name":name}))
    if line_string is not None:
        geo_line = extract_coordinates(line_string)
        bucket.append(Feature(geometry=LineString(geo_line),properties={"name":name,"timestamp":time_stamp} )) 
    if polygon is not None:  
        all_rings = []
        outer_ring = polygon.find('.kml:outerBoundaryIs/.kml:LinearRing', kml_namespace)
        all_rings.append(extract_coordinates(outer_ring))
        inner_rings = polygon.findall('.kml:innerBoundaryIs/.kml:LinearRing', kml_namespace)
        for inner_ring_elem in inner_rings:                
            all_rings.append(extract_coordinates(inner_ring_elem))
        bucket.append(Feature(geometry=Polygon(all_rings),properties={"name":name})) 
    if multigeometry is not None:
        points = multigeometry.findall('.kml:Point', kml_namespace)
        lines = multigeometry.findall('.kml:LineString', kml_namespace)
        polygons = multigeometry.findall('.kml:Polygon', kml_namespace)
        time_elem = multigeometry.find('.kml:TimeStamp/kml:when', kml_namespace)
        time_stamp = time_elem.text.strip() if time_elem is not None else None
        geometries_basket = []
        for point in points:
            geometries_basket.append(Point(extract_coordinates(point)[0]))
        for line in lines:
            geometries_basket.append(LineString(extract_coordinates(line)))
        for polygon in polygons:
            all_rings = []
            outer_ring = polygon.find('.kml:outerBoundaryIs/.kml:LinearRing', kml_namespace)
            all_rings.append(extract_coordinates(outer_ring))
            inner_rings = polygon.findall('.kml:innerBoundaryIs/.kml:LinearRing', kml_namespace)
            for inner_ring_elem in inner_rings:
                all_rings.append(extract_coordinates(inner_ring_elem))
            geometries_basket.append(Polygon(all_rings))
        geometries_collected = GeometryCollection(geometries_basket)
        bucket.append(Feature(geometry=geometries_collected, properties={"name":name,"timestamp":time_stamp}))

    if gx_track is not None:
        gx_coordinates = gx_track.findall('gx:coord', gx_namespace)
        coordinate_list=[]
        for lonlat in gx_coordinates:
            xyz = list(map(float, lonlat.text.split()))  # a list of 3 floats: longitude, latitude, elevation
            coordinate_list.append(xyz)  # collect all the gx:Track points
        list_tuples = [tuple(lst) for lst in coordinate_list]  # convert list of floats to list of tuples, feed LineString constructor    
        bucket.append(Feature(geometry=LineString(list_tuples),properties={"name":name,"timestamp":time_stamp} ))

output_string = pretty_dumps(FeatureCollection(bucket), indent=2, ensure_ascii=False)
# defaults to multi-line, human-readable geojson output
# if a one-line geojson is desired, delete ident=2 or run geo2geo-compact.py

with open(sys.argv[1]+'.geojson', 'w') as outfile:
    outfile.write( output_string )
print ( f"File saved as {sys.argv[1]+'.geojson'}")    