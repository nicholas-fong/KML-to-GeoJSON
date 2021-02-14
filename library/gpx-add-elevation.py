# add elevation data to gpx track, route, and waypoints
# GeoTiff files are stored on local drive

import sys
import gpxpy
import math
import rasterio
import numpy as np

filename = (sys.argv[1]+'.gpx')
with open( filename ) as infile:
    gpx = gpxpy.parse(infile)

def which_tile ( latitude, longitude ):
    if  ( latitude >= 0.0 and longitude >= 0.0 ):
        hemi, meri = "n", "e"
        t1 = f"{math.floor(latitude):02d}"
        t2 = f"{math.floor(longitude):03d}"
    elif ( latitude >= 0.0 and longitude < 0.0 ):
        hemi, meri = "n", "w"
        t1 = f"{math.floor(latitude):02d}"
        t2 = f"{math.ceil(abs(longitude)):03d}"
    elif ( latitude < 0.0 and longitude < 0.0 ):
        hemi, meri = "s", "w"
        t1 = f"{math.ceil(abs(latitude)):02d}"
        t2 = f"{math.ceil(abs(longitude)):03d}"
    elif ( latitude < 0.0 and longitude >= 0.0 ):
        hemi, meri = "s", "e"
        t1 = f"{math.ceil(abs(latitude)):02d}"
        t2 = f"{math.floor(longitude):03d}"
    return( f"{hemi}{t1}_{meri}{t2}.tif" ) 

def read_elevation(tiff_file, lat, lon):
    src=rasterio.open(tiff_file)
    array=src.read(1)
    y =src.width-1
    x =src.height-1
    if ( lat >= 0.0 ):
        x = round (x - lat%1 * x )
        y = round ( lon%1 * y )
        return array[ x, y ].astype(np.int16)
    if ( lat < 0.0 ):
        x = round ((1 - lat%1) * x )
        y = round ( lon%1 * y )
        return array[ x, y ].astype(np.int16)
            
# read gpx file and append elevation tags to 
# the gpx waypoints, route points and track points

for track in gpx.tracks: 
    for segment in track.segments:
        for p in segment.points:
            tiff_file=which_tile(p.latitude, p.longitude)
            z = read_elevation(tiff_file,p.latitude,p.longitude)
            p.elevation = z
                
for routes in gpx.routes:
    for p in routes.points:
        tiff_file=which_tile(p.latitude, p.longitude)
        z = read_elevation(tiff_file,p.latitude,p.longitude)
        p.elevation = z
        
for p in gpx.waypoints:
    tiff_file=which_tile(p.latitude, p.longitude)
    z = read_elevation(tiff_file,p.latitude,p.longitude)
    p.elevation = z

print (gpx.to_xml())
infile.close()
