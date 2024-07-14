# gpx waypoints are mapped to geoJSON Points
# gpx routes are mapped to geojson LineString
# gpx tracks are mapped to geojson LineString
# Note: gpx has no Polygons geometry
# gpx elevation, if exists, is added as the third parameter in geometry coordinates

import sys
import re
import gpxpy
from geojson import FeatureCollection, Feature, Point, LineString
import json

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
    with open( sys.argv[1]+'.gpx' ) as infile:
        gpx = gpxpy.parse(infile)
except FileNotFoundError:
    print("file not found")
    sys.exit(1) 

features = []    

for waypoint in gpx.waypoints:
    if waypoint.elevation:
        my_point = Point((waypoint.longitude, waypoint.latitude, int(waypoint.elevation)))
    else:
        my_point = Point((waypoint.longitude, waypoint.latitude))

    feature = Feature(geometry=my_point, properties={"name":waypoint.name, "sym":waypoint.symbol})
    features.append(feature)    

for route in gpx.routes: 
    route_list=[]
    for point in route.points:
        if point.elevation:
            route_list.append( (point.longitude, point.latitude, int(point.elevation)) )    
        else:
            route_list.append( (point.longitude, point.latitude) ) 
    feature = Feature(geometry=LineString(route_list), properties={"name":route.name})
    features.append(feature) 

for track in gpx.tracks: 
    for segment in track.segments:
        track_list=[]
        for point in segment.points:
            if point.elevation:
                track_list.append( (point.longitude, point.latitude, int(point.elevation)) )
            else:
                track_list.append( (point.longitude, point.latitude))
        feature = Feature(geometry=LineString(track_list), properties={"name":track.name})
        features.append(feature)   

output_string = custom_dumps(FeatureCollection(features), indent=2, ensure_ascii=False)

#print(output_string)
with open(sys.argv[1]+'.geojson', 'w') as outfile:
    outfile.write( output_string )
