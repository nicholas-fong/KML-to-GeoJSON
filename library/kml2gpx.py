# Convert KML Point, LineString, MultiGeometry Point LineString to GPX

import sys
import xml.etree.ElementTree as ET
import re
import gpxpy.gpx

kml_namespace = {'kml': 'http://www.opengis.net/kml/2.2'} 

gpxbucket = gpxpy.gpx.GPX()   #create a gpx object

# function to extract coordinates from a kml geometry element and returns a list of tuples
def extract_coordinates(geometry_element):
    coordinates_elem = geometry_element.find('.//kml:coordinates', kml_namespace)
    if coordinates_elem is not None:
        # coordinates is a list of strings
        coordinates = coordinates_elem.text.strip().split()
        # convert to a list of tuples
        list_of_tuples = [tuple(map(float, item.split(','))) for item in coordinates]
        return list_of_tuples

try:
    with open(sys.argv[1]+".kml") as infile:
        tree = ET.parse(infile)
except FileNotFoundError:
    print(f"Error: File {sys.argv[1]}.kml not found.")
    sys.exit(1)
except ET.ParseError:
    print("Error: Failed to parse the KML file.")
    sys.exit(1)

root = tree.getroot()

def process_placemarks(root, kml_namespace, gpxbucket):
    for placemark in root.findall('.//kml:Placemark', kml_namespace):
        name = get_name(placemark, kml_namespace)
        process_points(placemark, name, kml_namespace, gpxbucket)
        process_line_strings(placemark, name, kml_namespace, gpxbucket)

def get_name(placemark, kml_namespace):
    name_elem = placemark.find('.kml:name', kml_namespace)
    return name_elem.text.strip() if name_elem is not None else 'Unnamed'

def process_points(placemark, name, kml_namespace, gpxbucket):
    points = placemark.findall('.//kml:Point', kml_namespace)
    for point in points:
        point_coords = extract_coordinates(point)
        new_wpt = gpxpy.gpx.GPXWaypoint(
            name=name,
            latitude=point_coords[0][1],
            longitude=point_coords[0][0]
        )
        gpxbucket.waypoints.append(new_wpt)

def process_line_strings(placemark, name, kml_namespace, gpxbucket):
    line_strings = placemark.findall('.//kml:LineString', kml_namespace)
    for line_string in line_strings:
        new_route = gpxpy.gpx.GPXRoute(name)
        gpxbucket.routes.append(new_route)
        line_coords = extract_coordinates(line_string)
        for coord in line_coords:
            new_route.points.append(gpxpy.gpx.GPXRoutePoint(coord[1], coord[0]))

# Call the function with your parameters
process_placemarks(root, kml_namespace, gpxbucket)

print( gpxbucket.to_xml() )
