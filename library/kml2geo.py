# Convert KML Point, LineString, Polygon  to GeoJSON, also handles kml gx:Track and convert to LineString.
import sys
import xml.etree.ElementTree as ET
from geojson import FeatureCollection, Feature, Point, LineString, Polygon, GeometryCollection
import json

kml_namespace = {'kml': 'http://www.opengis.net/kml/2.2'} 
gx_namespace =  {'gx': 'http://www.google.com/kml/ext/2.2'}

features=[]

# function to extract coordinates from a kml geometry element and returns a list of tuples
def extract_coordinates(geometry_element):
    coordinates_elem = geometry_element.find('kml:coordinates', kml_namespace)
    if coordinates_elem is not None:
        # coordinates is a list of strings
        coordinates = coordinates_elem.text.strip().split()
        # convert to a list of tuples
        list_of_tuples = [tuple(map(float, item.split(','))) for item in coordinates]
        return list_of_tuples
    
with open(sys.argv[1]+".kml") as infile:
    tree = ET.parse(infile)
root = tree.getroot()

# Find all placemark elements
for placemark in root.findall('.//kml:Placemark', kml_namespace):
    name_elem = placemark.find('kml:name', kml_namespace)
    name = name_elem.text.strip() if name_elem is not None else 'Unnamed'
    time_elem = placemark.find('kml:TimeStamp/kml:when', kml_namespace)
    time_stamp = time_elem.text.strip() if time_elem is not None else None

    # Check for geometry types: Point, LineString, Polygon, MultiGeometry or gx_track
    point = placemark.find('kml:Point', kml_namespace)
    line_string = placemark.find('kml:LineString', kml_namespace)
    polygon = placemark.find('kml:Polygon', kml_namespace)
    multigeometry = placemark.find('kml:MultiGeometry', kml_namespace)
    gx_track = placemark.find('gx:Track', gx_namespace)

    if point:
        geo_point = extract_coordinates(point)
        features.append(Feature(geometry=Point(geo_point[0]), properties={"name":name}))
    if line_string:
        geo_line = extract_coordinates(line_string)
        features.append(Feature(geometry=LineString(geo_line),properties={"name":name,"timestamp":time_stamp} )) 
    if polygon:
        all_rings = []
        outer_ring = polygon.find('kml:outerBoundaryIs/kml:LinearRing', kml_namespace)
        all_rings.append(extract_coordinates(outer_ring))
        inner_rings = polygon.findall('kml:innerBoundaryIs/kml:LinearRing', kml_namespace)
        for inner_ring_elem in inner_rings:                
            all_rings.append(extract_coordinates(inner_ring_elem))
        features.append(Feature(geometry=Polygon(all_rings),properties={"name":name})) 

    if gx_track:
        gx_coordinates = gx_track.findall('gx:coord', gx_namespace)
        coordinate_list=[]
        for lonlat in gx_coordinates:
            xyz = list(map(float, lonlat.text.split()))  # a list of 3 floats: longitude, latitude, elevation
            coordinate_list.append(xyz)  # collect all the gx:Track points
        list_tuples = [tuple(lst) for lst in coordinate_list]  # convert list of floats to list of tuples, feed LineString constructor    
        features.append(Feature(geometry=LineString(list_tuples),properties={"name":name,"timestamp":time_stamp} ))


geojson_string = json.dumps(FeatureCollection(features), indent=2, ensure_ascii=False)
# defaults to multi-line, human-readable geojson output
# if a one-line geojson is desired, comment out above line, uncomment the line below.
# geojson_string = json.dumps(FeatureCollection(features), ensure_ascii=False)

#print(geojson_string)
with open(sys.argv[1]+'.geojson', 'w') as outfile:
    outfile.write( geojson_string )
