import sys
from pykml import parser
import simplekml

kml = simplekml.Kml()
#Parse Google KML map and save as a basic KML file with no bells and whistles. Basic KML

def process(params):
    for j in params:
        try:
            lonlat = str(j.Point.coordinates).split(',')
        except:
            pass
        else:    
            longitude = float(lonlat[0])
            latitude = float(lonlat[1])
            try:
                label = str(j.name)
            except:
                label = "noname"
            mypoint = kml.newpoint(name=label)
            mypoint.coords = [ (longitude, latitude)  ]
        try:
            coord_array = (j.LineString.coordinates).text.split("\n") # parse coordinates to a list of substrings
            if (len(coord_array)==1):               #some KML coordinates are arranged in one line
                coord_array=coord_array[0].split()  #break up single line coordinates to a list of str elements
            coord_array = [ item.strip() for item in coord_array if item !='' ]    # get rid of very messy LF and whitespaces
            coord_array = [ item for item in coord_array if item !='' ]            # do it one more time to remove residual null string
            # finally a list of strings: e.g.  ['-123,49', '-123,49', '-123,49']
            # convert to a list of floats: e.g. [[-123,49], [-123,49], [-123,49]] 
            # conventional approach:
            #   list_of_floats=[]
            #   for item in coord_array:
            #       xyz = [float(j) for j in item.split(',')]
            #       list_of_floats.append(xyz)
            # use "list comprehension" to convert list of str to list of float
            my_floats = [list(map(float, item.split(','))) for item in coord_array] 
            try:
                label = str(j.name)
            except:
                label = ''
            myline = kml.newlinestring(name=label)
            myline.coords = my_floats
        except:
            pass
        try:
            coord_array = (j.Polygon.outerBoundaryIs.LinearRing.coordinates).text.split("\n") # parse coordinates to a list of substrings
            if (len(coord_array)==1):               #some KML coordinates are arranged in one line
                coord_array=coord_array[0].split()  #break up single line coordinates to a list of str elements
            coord_array = [ item.strip() for item in coord_array if item !='' ]    # get rid of very messy LF and whitespaces
            coord_array = [ item for item in coord_array if item !='' ]            # do it one more time to remove residual null string
            # finally a list of strings: e.g.  ['-123,49', '-123,49', '-123,49']
            # convert to a list of floats: e.g. [[-123,49], [-123,49], [-123,49]] 
            my_poly = [list(map(float, item.split(','))) for item in coord_array]  
            try:
                label = str(j.name)
            except:
                label = ''
            mypoly = kml.newpolygon(name=label)    
            mypoly.outerboundaryis = my_poly
        except:
            pass

#main() here
if len(sys.argv) < 2:
    print("Enter a kml file to convert to GeoJSON ")
    sys.exit(1)

with open(sys.argv[1]+".kml") as infile:
    root = parser.parse(infile).getroot()
infile.close()

try:
    process(root.Document.Placemark) # nice clean minimalist KML structure
except:
    try:
        process(root.Document.Folder.Placemark) # Google, Avenza KML include Folder structure
    except:
        try:
            process(root.Document.Document.Placemark) # ogr2ogr LIBKML drv has nested document folders
        except:
            pass  # may come across other wild KML structures, add it here if possible. If all else fails, use ogr2ogr

#print(kml.kml())
kml.save(sys.argv[1]+"-min.kml")


