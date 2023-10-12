# gpx waypoints are mapped to geoJSON Points
# gpx routes and gpx tracks are treated equally: mapped to geojson LineString
# gpx route and gpx track are mapped as a LineString each
# gpx has no Polygons geometry, therefore GeoJSON file will have no polygons
# gpx elevation if exists is added as the third parameter in geometry coordinates

import sys
import gpxpy
import gpxpy.gpx
from geojson import FeatureCollection, Feature, Point, LineString, dumps

with open( sys.argv[1]+'.gpx' ) as infile:
    gpx = gpxpy.parse(infile)
infile.close()    
    
basket = []    

for waypoint in gpx.waypoints:
    lat = float(waypoint.latitude)
    lon = float(waypoint.longitude)
    if waypoint.elevation:
        my_point = Point((lon, lat, waypoint.elevation))
    else:
        my_point = Point((lon, lat))

    my_feature = Feature(geometry=my_point, properties={"name":waypoint.name})
    basket.append(my_feature)    

for route in gpx.routes: 
    array=[]
    for point in route.points:
        if point.elevation:
            array.append( (point.longitude, point.latitude, point.elevation) )    
        else:
            array.append( (point.longitude, point.latitude) ) 
    my_line = LineString(array)
    my_feature = Feature(geometry=my_line, properties={"name":route.name})
    basket.append(my_feature) 

for track in gpx.tracks: 
    varname = track.name
    for segment in track.segments:
        array=[]
        for point in segment.points:
            if point.elevation:
                array.append( (point.longitude, point.latitude, point.elevation) )
            else:
                array.append( (point.longitude, point.latitude))
        my_line = LineString(array)
        my_feature = Feature(geometry=my_line, properties={"name":track.name})
        basket.append(my_feature)   

geojson_string = dumps(FeatureCollection(basket), indent=2, ensure_ascii=False)
print(geojson_string)

with open(sys.argv[1]+'.geojson', 'w') as outfile:
    outfile.write( geojson_string )
