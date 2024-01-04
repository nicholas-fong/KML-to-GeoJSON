# input asc file and convert each line (lat, lon) to gpx route point

import sys
import csv
import gpxpy.gpx as hiking

gpx = hiking.GPX()                   #create a new GPX object called gpx

route_name = input ("What do you want to call the route ?  ") 

# Create a route segment
route = hiking.GPXRoute(route_name) 
gpx.routes.append(route)  

with open(sys.argv[1]+'.asc' ) as f:
    readline = csv.reader(f, delimiter=',', quotechar='"')
    for row in readline:
        if row:           # Create a route point
            route_point = hiking.GPXRoutePoint(latitude=float(row[0]),longitude=float(row[1]))
            route_point.elevation = 0.0
            route.points.append(route_point)  # Add the route point to the route

#print( gpx.to_xml())

with open(sys.argv[1]+'.gpx', 'w') as outfile:
    outfile.write( gpx.to_xml() )

