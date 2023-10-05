# gpx waypoint is mapped to geoJSON Point
# gpx routes and gpx tracks are mapped to geojson LineString
# gpx has no Polygons geometry
# gpx elevation if exists is added as the third parameter in geometry

import sys
import gpxpy
import gpxpy.gpx
from geojson import FeatureCollection, Feature, Point, LineString
import json

with open( sys.argv[1]+'.gpx' ) as infile:
    gpx = gpxpy.parse(infile)
infile.close()    
    
basket = []    

for waypoint in gpx.waypoints:
    lat = float(waypoint.latitude)
    lon = float(waypoint.longitude)
    varname = waypoint.name
    if waypoint.elevation is None:
        my_point = Point((lon, lat))
    else:
        my_point = Point((lon, lat, waypoint.elevation))

    my_feature = Feature(geometry=my_point, properties={"name":varname})
    basket.append(my_feature)    

for route in gpx.routes: 
    varname = route.name
    array=[]
    for point in route.points:
        if point.elevation is None:
            array.append( (point.longitude, point.latitude) )    
        else:
            array.append( (point.longitude, point.latitude, point.elevation) ) 
    my_line = LineString(array)
    my_feature = Feature(geometry=my_line, properties={"name":varname})
    basket.append(my_feature) 

for track in gpx.tracks: 
    varname = track.name
    for segment in track.segments:
        array=[]
        for point in segment.points:
            if point.elevation is None:
                array.append( (point.longitude, point.latitude) )
            else:
                array.append( (point.longitude, point.latitude, point.elevation))
        my_line = LineString(array)
        my_feature = Feature(geometry=my_line, properties={"name":varname})
        basket.append(my_feature)   

geojson_string = json.dumps(FeatureCollection(basket), indent=2, ensure_ascii=False)
print(geojson_string)

with open(sys.argv[1]+'.geojson', 'w') as outfile:
    outfile.write( geojson_string )
