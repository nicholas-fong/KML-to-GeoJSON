# gpx waypoints are mapped to geoJSON Points
# gpx routes mapped to geojson LineString
# gpx tracks mapped to geojson LineString
# gpx has no Polygons
# gpx elevation if exists is added as the third parameter in geometry coordinates

import sys
import gpxpy
import gpxpy.gpx
from geojson import FeatureCollection, Feature, Point, LineString
import json

with open( sys.argv[1]+'.gpx' ) as infile:
    gpx = gpxpy.parse(infile)
infile.close()    
    
features = []    

for waypoint in gpx.waypoints:
    lat = float(waypoint.latitude)
    lon = float(waypoint.longitude)
    if waypoint.elevation:
        my_point = Point((lon, lat, waypoint.elevation))
    else:
        my_point = Point((lon, lat))

    feature = Feature(geometry=my_point, properties={"name":waypoint.name})
    features.append(feature)    

for route in gpx.routes: 
    route_list=[]
    for point in route.points:
        if point.elevation:
            route_list.append( (point.longitude, point.latitude, point.elevation) )    
        else:
            route_list.append( (point.longitude, point.latitude) ) 
    feature = Feature(geometry=LineString(route_list), properties={"name":route.name})
    features.append(feature) 

for track in gpx.tracks: 
    for segment in track.segments:
        track_list=[]
        for point in segment.points:
            if point.elevation:
                track_list.append( (point.longitude, point.latitude, point.elevation) )
            else:
                track_list.append( (point.longitude, point.latitude))
        feature = Feature(geometry=LineString(track_list), properties={"name":track.name})
        features.append(feature)   

geojson_string = json.dumps(FeatureCollection(features), indent=2, ensure_ascii=False)
#print(geojson_string)

with open(sys.argv[1]+'.geojson', 'w') as outfile:
    outfile.write( geojson_string )
