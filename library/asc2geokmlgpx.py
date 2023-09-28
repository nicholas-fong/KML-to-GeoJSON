# input a CSV (asc) file and create corresponding GeoJSON, KML and GPX (Waypoints) files.
# CSV (asc) file has 3 columns, latitude, longitude and name of the geo location (Point)
# the third column (name field) can be quoted or unquoted
# create a .geojson file, a .kml file and a .gpx file
# assume CSV data is WGS84 latitude and longitude
# quotation marks in third column (name field) are optional and are filtered out, but don't use comma in this field.
# leading and trailing blanks in name filed are also filtered out
# additional columns beyond column 3 are ignored
# Note: no elevation data, they are default to 0 

import sys
import csv
import json
from geojson import FeatureCollection, Feature, Point
import simplekml
import gpxpy

if len(sys.argv) < 2:
    print("Please enter a CSV file. File extension .asc is assumed") 
    sys.exit(1)

basket = []             # empty basket to hold/collect features
kml = simplekml.Kml()   # new KML object to hold/collect points/Placemark
obj = gpxpy.gpx.GPX()   # create a gpx overall object
                        # folder = kml.newfolder(name='MyFolder')

with open(sys.argv[1]+'.asc') as infile:
    reader = csv.reader(infile, delimiter=',')
    for row in reader:
        if row:         # an extra statement to filter out empty lines
            my_name=row[2].replace('"', '').strip()
            lat = float(row[0])
            lon = float(row[1])
            elev = 0.0    
            my_point=Point([lon,lat,elev])
            basket.append(Feature(geometry=my_point, properties={"name":my_name}))  #add to features basket
            kml.newpoint(name=my_name, coords=[(lon,lat,elev)])                     #add to kml placemark
            wpt = gpxpy.gpx.GPXWaypoint()                                           #instantiate a Waypoint object        
            wpt.latitude = lat
            wpt.longitude = lon
            wpt.elevation = elev
            wpt.name = my_name
            obj.waypoints.append(wpt)

geo_string = json.dumps( FeatureCollection(basket), indent=2, ensure_ascii=False )

with open(sys.argv[1]+'.geojson', 'w') as outfile:
    outfile.write( geo_string )

kml.save(sys.argv[1]+".kml")

with open(sys.argv[1]+'.gpx', 'w') as outfile:
    outfile.write( obj.to_xml() )

print(geo_string)
print(kml.kml())
print( obj.to_xml())

