# https://overpass-turbo.eu/ exports query result to GeoJSON format.
# JOSM can export to GeoJSON format.
# convert GeoJSON Points to gpx waypoints, add elevation if exists.
# convert GeoJSON LineStrings to a gpx track, add elevation if exists.
# convert GeoJSON Polygons to a waypoint (based on centroid of the polygon vertices), no elevation.

import sys
from statistics import mean
import geojson
import gpxpy.gpx

if len(sys.argv) < 2:
    print("Please enter a geojson filename. Points, LineStrings and Polygon (point centroid) are converted ") 
    sys.exit(1)

custom_symbol = input( "GeoJSON to GPX, if symbol is missing, enter a custom symbol  ")

with open( sys.argv[1]+'.geojson', 'r') as infile:
   data = geojson.load ( infile )

new = gpxpy.gpx.GPX()   #create a gpx object

for i in range(len(data['features'])):
    geom = data['features'][i]['geometry']
    node = geom['coordinates']
    
    if ( geom['type'] == 'Point' ):
        new_wpt = gpxpy.gpx.GPXWaypoint()    # create new point object
        try:                      # can also use properties.get()  cleaner code
            myname = data['features'][i]['properties']['name']
        except:
            try:
                myname = data['features'][i]['properties']['Name']
            except:
                myname = 'noname'
        new_wpt.name = myname

        try:
            existing_symbol = data['features'][i]['properties']['sym']
        except:
            existing_symbol = 'empty'

        if ( existing_symbol != 'empty'):
            new_wpt.symbol = existing_symbol
        else:    
            if (custom_symbol != None):
                new_wpt.symbol = custom_symbol
        
        if (len(node)) == 2:
            new_wpt.latitude = node[1]
            new_wpt.longitude = node[0]
        else:    
            new_wpt.latitude = node[1]
            new_wpt.longitude = node[0]
            new_wpt.elevation = node[2]    
        new.waypoints.append(new_wpt)

    if ( geom['type'] == 'LineString' ):
        try:
            myname = data['features'][i]['properties']['name']
        except:
            try:
                myname = data['features'][i]['properties']['Name']
            except:
                myname = 'noname'
        new_route =  gpxpy.gpx.GPXRoute( myname )       
        new.routes.append(new_route)

        for j in range(len(node)):
            if (len(node[j])) == 2:
                new_route.points.append(gpxpy.gpx.GPXRoutePoint(node[j][1],node[j][0]))
            else:
                new_route.points.append(gpxpy.gpx.GPXRoutePoint(node[j][1],node[j][0],node[j][2]))   

                
    if ( geom['type'] == 'Polygon' ):     # if Polygon, calculate centroid and consider it as a Point
        new_wpt = gpxpy.gpx.GPXWaypoint()
        pnode = data['features'][i]['geometry']['coordinates'][0]
        bucket1=[]
        bucket2=[]
        for j in range(len(pnode)-1):
            bucket1.append( pnode[j][1] )
            bucket2.append( pnode[j][0] )
        try:
            myname = data['features'][i]['properties']['name']
        except:
            try:
                myname = data['features'][i]['properties']['Name']
            except:
                myname = 'noname'
        new_wpt.name = myname
        new_wpt.latitude = mean(bucket1)
        new_wpt.longitude = mean(bucket2)
        new.waypoints.append(new_wpt)

#print( new.to_xml() )
with open(sys.argv[1]+'.gpx', 'w') as file:
    file.write( new.to_xml() )
print ( f"File saved as {sys.argv[1]+'.gpx'}")
