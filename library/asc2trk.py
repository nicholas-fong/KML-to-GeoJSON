# input asc file and convert each line (lat, lon) to gpx track point

import sys
import csv
import gpxpy
import gpxpy.gpx

gpx = gpxpy.gpx.GPX()

track_name = input ("What do you want to call the track ?  ") 

track = gpxpy.gpx.GPXTrack(track_name)  #create a new track
gpx.tracks.append(track)                #commit the new track

segment = gpxpy.gpx.GPXTrackSegment()   #create a new track segment
track.segments.append(segment)          #commit the new track segment

with open( sys.argv[1]+'.asc' ) as f:
    readline = csv.reader(f, delimiter=',', quotechar='"')
    for i in readline:
        if i:
            # Create a track point
            track_point = gpxpy.gpx.GPXTrackPoint( float(i[0]), float(i[1])  )
            track_point.elevation = 0.0
            segment.points.append(track_point)

print( gpx.to_xml())

with open(sys.argv[1]+'.gpx', 'w') as outfile:
    outfile.write( gpx.to_xml() )

