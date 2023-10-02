# input asc file and convert each line (lat, lon, name) to a gpx waypoint

import sys
import csv
import gpxpy

if len(sys.argv) < 2:
    print("Please enter a CSV file. File extension .asc is assumed") 
    sys.exit(1)

new = gpxpy.gpx.GPX()

with open(sys.argv[1]+'.asc') as f:
    reader = csv.reader(f, delimiter=',', quotechar='"')
    for row in reader:
        if row:         # an extra statement to filter out empty lines
            wpt = gpxpy.gpx.GPXWaypoint( float(row[0]), float(row[1]) )
            wpt.name = row[2].replace('"', '').strip()
            wpt.elevation = 0.0            
            new.waypoints.append(wpt)

with open(sys.argv[1]+'.gpx', 'w') as outfile:
    outfile.write( new.to_xml() )

print( new.to_xml())
