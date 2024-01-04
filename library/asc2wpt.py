# input asc file and convert each line (lat, lon, name) to a gpx waypoint

import sys
import csv
import gpxpy.gpx as hiking

gpx = hiking.GPX()                   #create a new GPX object called gpx

if len(sys.argv) < 2:
    print("Please enter a CSV file. File extension .asc is assumed") 
    sys.exit(1)

with open(sys.argv[1]+'.asc') as f:
    reader = csv.reader(f, delimiter=',', quotechar='"')
    for row in reader:
        if row:         # an extra statement to filter out empty lines
            wpt = hiking.GPXWaypoint( float(row[0]), float(row[1]) )
            try:
                wpt.name = row[2].replace('"', '').strip()
            except:
                wpt.name = None    
            wpt.elevation = 0.0            
            gpx.waypoints.append(wpt)

#print( gpx.to_xml())

with open(sys.argv[1]+'.gpx', 'w') as outfile:
    outfile.write( gpx.to_xml() )
