import sys
from pykml import parser
import json
from geojson import FeatureCollection, Feature, Point, LineString, Polygon
# parsed kml coordinates, convert to text, split into substrings, in a single line situation, break it up.
# clean up ultra messy separators (some use LF, some use LF and spaces). Result is a "clean" list of strings. 
# use list comprehension, create a list floats from list of strings. Feed it to LineString geometry constructor. 
# GeoJSON polygon coordinates requires extra square brackets [[    ]] to make a list of lists. 
# Polygon: first element of a list of lists is the list of Polygon outer-ring coordinates.
# KML tag Polygon.outerBoundaryIs.LinearRing.coordinates

def process_features(set_of_features):
    for j in set_of_features:           
        try:
            lonlat = (j.Point.coordinates).text.split(',')
            try:
                label = str(j.name)
            except:
                label = ''    
            try:
                my_point=Point([float(lonlat[0]),float(lonlat[1]),float(lonlat[2])])
            except:
                my_point=Point([float(lonlat[0]),float(lonlat[1])])
            #convert to a gemoetry Point object ==> dictionary with key "coordinates"
            basket.append(Feature(geometry=my_point, properties={"name":label}))
        except:
            pass
 
    for j in set_of_features:  
    # Process minimalist kml style, Google kml style, Avenza kml style, brouter kml style, 
    # ogr2ogr kml style and mapshaper kml    
        try:
            coord_array = (j.LineString.coordinates).text.split("\n") # create list of substrings
            if (len(coord_array)==1):               #some KML coordinates are arranged in one line
                coord_array=coord_array[0].split()  #break up single line to list of str elements
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
            try:
                time_str=str(j.TimeStamp.when)
            except:
                time_str=''
            if (time_str == "none"):
                basket.append(Feature(geometry=LineString(my_floats),properties={"name":label} ))
            else:
                basket.append(Feature(geometry=LineString(my_floats),properties={"name":label,"timestamp":time_str} ))      
        except:
            pass

    for j in set_of_features:            
        try:
            coord_array = (j.Polygon.outerBoundaryIs.LinearRing.coordinates).text.split("\n")
            if (len(coord_array)==1):               #some KML coordinates are arranged in one line
                coord_array=coord_array[0].split()  #break up single line to list of str elements
            coord_array = [ item.strip() for item in coord_array if item !='' ]    # get rid of very messy LF and whitespaces
            coord_array = [ item for item in coord_array if item !='' ]            # do it one more time to remove residual null string
            # finally a list of strings: e.g.  ['-123,49', '-123,49', '-123,49']
            # convert to a list of floats: e.g. [[-123,49], [-123,49], [-123,49]] 
            my_poly = [[list(map(float, item.split(','))) for item in coord_array]]  #double square brackets needed
            try:
                label = str(j.name)
            except:
                label = ''      
            basket.append(Feature(geometry=Polygon(my_poly),properties={"name":label}  ))  
        except:
            pass

# main()
print ("For simple kml files only. For more complex files, use 'ogr2ogr sample.geojson sample.kml' ")

if len(sys.argv) < 2:
    print("Enter a kml file to convert to GeoJSON ")
    sys.exit(1)

with open(sys.argv[1]+".kml") as f:
    root = parser.parse(f).getroot()
f.close()    
# KML comes different sizes and shapes and it gets ugrly very quickly, in that case
# use GDAL ogr2ogr to do the conversion
basket = []  # yes this is a global variable: to make things simple.
try:
    process_features(root.Document.Placemark) # nice clean minimalist KML structure
except:
    try:
        process_features(root.Document.Folder.Placemark) # Google, Avenza KML include Folder structure
    except:
        try:
            process_features(root.Document.Document.Placemark) # ogr2ogr LIBKML drv has nested document folders
        except:
            pass  # may come across other wild KML structures, add it here if possible. If all else fails, use ogr2ogr

geojson_string = json.dumps(FeatureCollection(basket), indent=2, ensure_ascii=False)
print(geojson_string)

with open(sys.argv[1]+'.geojson', 'w') as outfile:
    outfile.write( geojson_string )
