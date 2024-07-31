# https://overpass-turbo.eu/ exports query result to GeoJSON format.
# JOSM can export to GeoJSON format.
# convert GeoJSON Points to gpx waypoints, add elevation if exists.
# convert GeoJSON LineStrings to a gpx track, add elevation if exists.
# convert GeoJSON Polygons to a Waypoint (based on the centroid of the Polygon vertices), no elevation.

import sys
from statistics import mean
import json
import gpxpy.gpx

if len(sys.argv) < 2:
    print("Enter a GeoJSON file ") 
    sys.exit(1)
print("Special Note: Polygon, if exists, its centroid is mapped to Waypoint ") 
custom_symbol = input( "Eenter an optional Garmin symbol, e.g. Waypoint   : ")

try:
    with open(sys.argv[1] + '.geojson', 'r') as infile:
        data = json.load(infile)
except FileNotFoundError:
    print(f"Error: File {sys.argv[1]}.geojson not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print("Error: Failed to parse GeoJSON file.")
    sys.exit(1)

def get_property(properties, key, default='noname'):
    return properties.get(key) or properties.get(key.capitalize(), default)

def process_point(geom, properties, custom_symbol, gpx):
    node = geom['coordinates']
    new_wpt = gpxpy.gpx.GPXWaypoint()
    new_wpt.name = get_property(properties, 'name')
    new_wpt.symbol = properties.get('sym', custom_symbol) if properties.get('sym') != 'empty' else custom_symbol
    new_wpt.latitude, new_wpt.longitude = node[1], node[0]
    if len(node) == 3:
        new_wpt.elevation = node[2]
    gpx.waypoints.append(new_wpt)

def process_linestring(geom, properties, gpx):
    node = geom['coordinates']
    new_route = gpxpy.gpx.GPXRoute(get_property(properties, 'name'))
    gpx.routes.append(new_route)
    for coord in node:
        new_route.points.append(gpxpy.gpx.GPXRoutePoint(coord[1], coord[0], coord[2] if len(coord) == 3 else None))

def process_polygon(geom, properties, gpx):
    pnode = geom['coordinates'][0]
    bucket1, bucket2 = zip(*[(coord[1], coord[0]) for coord in pnode[:-1]])
    new_wpt = gpxpy.gpx.GPXWaypoint(
        name=get_property(properties, 'name'),
        latitude=mean(bucket1),
        longitude=mean(bucket2)
    )
    gpx.waypoints.append(new_wpt)

def process_multipoint(geom, properties, custom_symbol, gpx):
    for point in geom['coordinates']:
        process_point({'coordinates': point, 'type': 'Point'}, properties, custom_symbol, gpx)

def process_multilinestring(geom, properties, gpx):
    for linestring in geom['coordinates']:
        process_linestring({'coordinates': linestring, 'type': 'LineString'}, properties, gpx)

def process_multipolygon(geom, properties, gpx):
    for polygon in geom['coordinates']:
        process_polygon({'coordinates': polygon, 'type': 'Polygon'}, properties, gpx)

def process_geometrycollection(geom, properties, custom_symbol, gpx):
    for geometry in geom['geometries']:
        process_geometry(geometry, properties, custom_symbol, gpx)

def process_geometry(geom, properties, custom_symbol, gpx):
    geom_type = geom['type']
    if geom_type == 'Point':
        process_point(geom, properties, custom_symbol, gpx)
    elif geom_type == 'LineString':
        process_linestring(geom, properties, gpx)
    elif geom_type == 'Polygon':
        process_polygon(geom, properties, gpx)
    elif geom_type == 'MultiPoint':
        process_multipoint(geom, properties, custom_symbol, gpx)
    elif geom_type == 'MultiLineString':
        process_multilinestring(geom, properties, gpx)
    elif geom_type == 'MultiPolygon':
        process_multipolygon(geom, properties, gpx)
    elif geom_type == 'GeometryCollection':
        process_geometrycollection(geom, properties, custom_symbol, gpx)

# main()
gpx = gpxpy.gpx.GPX()
for feature in data['features']:
    geom = feature['geometry']
    properties = feature['properties']
    process_geometry(geom, properties, custom_symbol, gpx)

with open(sys.argv[1]+'.gpx', 'w') as outfile:
    outfile.write( gpx.to_xml() )
print ( f"File saved as {sys.argv[1]+'.gpx'}")  