# Convert KML Point, LineString, MultiGeometry Point LineString to GPX
# Polygon centroid is mapped to a Waypoint
import sys
import xml.etree.ElementTree as ET
import re
import gpxpy.gpx
from typing import List, Tuple

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

def find_polygon_centroid(vertices: List[Tuple[float, float]]) -> Tuple[float, float]:
    x_list = [vertex[0] for vertex in vertices]
    y_list = [vertex[1] for vertex in vertices]
    n = len(vertices) - 1  # The last vertex is the same as the first one to close the polygon
    # Calculate the signed area of the polygon
    A = 0.5 * sum(x_list[i] * y_list[i+1] - x_list[i+1] * y_list[i] for i in range(n))
    # Calculate the centroid coordinates
    C_x = (1 / (6 * A)) * sum((x_list[i] + x_list[i+1]) * (x_list[i] * y_list[i+1] - x_list[i+1] * y_list[i]) for i in range(n))
    C_y = (1 / (6 * A)) * sum((y_list[i] + y_list[i+1]) * (x_list[i] * y_list[i+1] - x_list[i+1] * y_list[i]) for i in range(n))
    return C_x, C_y

def get_name(placemark, kml_namespace):
    name_elem = placemark.find('.kml:name', kml_namespace)
    return name_elem.text.strip() if name_elem is not None else 'Unnamed'

def process_points(placemark, name, kml_namespace, gpxbucket):
    points = placemark.findall('.//kml:Point', kml_namespace)
    for point in points:
        point_coords = extract_coordinates(point)
        new_wpt = gpxpy.gpx.GPXWaypoint(name=name, latitude=point_coords[0][1],longitude=point_coords[0][0])
        gpxbucket.waypoints.append(new_wpt)

def process_line_strings(placemark, name, kml_namespace, gpxbucket):
    line_strings = placemark.findall('.//kml:LineString', kml_namespace)
    for line_string in line_strings:
        new_route = gpxpy.gpx.GPXRoute(name)
        gpxbucket.routes.append(new_route)
        line_coords = extract_coordinates(line_string)
        for coord in line_coords:
            new_route.points.append(gpxpy.gpx.GPXRoutePoint(coord[1], coord[0]))

def process_polygon (placemark, name, kml_namespace, gpxbucket):
    polygons = placemark.findall('.//kml:Polygon', kml_namespace)
    for polygon in polygons:
        outer_ring = polygon.find('.kml:outerBoundaryIs/kml:LinearRing', kml_namespace)
        polygon_vertex = extract_coordinates(outer_ring)
        centroid = find_polygon_centroid(polygon_vertex)
        new_wpt = gpxpy.gpx.GPXWaypoint(name = name + " (centroid)", latitude=centroid[1], longitude=centroid[0])
        gpxbucket.waypoints.append(new_wpt) 

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

for placemark in root.findall('.//kml:Placemark', kml_namespace):
    name = get_name(placemark, kml_namespace)
    process_points(placemark, name, kml_namespace, gpxbucket)
    process_line_strings(placemark, name, kml_namespace, gpxbucket)
    process_polygon(placemark, name, kml_namespace, gpxbucket)

#print( gpxbucket.to_xml() )
with open(sys.argv[1]+'.gpx', 'w') as outfile:
    outfile.write( gpxbucket.to_xml() )
print ( f"File saved as {sys.argv[1]+'.gpx'}")      
