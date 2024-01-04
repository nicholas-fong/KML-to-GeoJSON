# input asc file and convert each line (lat, lon) to gpx track point

import sys
import csv
import gpxpy.gpx as hiking

gpx = hiking.GPX()                   #create a new GPX object called gpx

track_name = input ("What do you want to call the track ?  ") 

track = hiking.GPXTrack(track_name)  #create a new track
gpx.tracks.append(track)             #add track to gpx

segment = hiking.GPXTrackSegment()   #create a new track segment
track.segments.append(segment)       #add new track segment

with open( sys.argv[1]+'.asc' ) as f:
    readline = csv.reader(f, delimiter=',', quotechar='"')
    for row in readline:
        if row:
            # Create a track point
            track_point = hiking.GPXTrackPoint( float(row[0]), float(row[1])  )
            track_point.elevation = 0.0
            segment.points.append(track_point)

#print( gpx.to_xml())

with open(sys.argv[1]+'.gpx', 'w') as outfile:
    outfile.write( gpx.to_xml() )

