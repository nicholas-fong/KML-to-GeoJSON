import sys
from pykml import parser
import json
from geojson import FeatureCollection, Feature, Point, LineString, Polygon

# tricky data type, tricky conversions and tricky element access: 
# Polygon.outerBoundaryIs.LinearRing.coordinates
# kml coordinates, convert to text, split into elements, remove null elements, split, create list float, create LineString object
# note: GeoJSON polygon coordinates requires extra square brackets  [[   ]] it is a list of lists

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
 
    for j in set_of_features:  # clumsy code but kind of works. 
    #Process basic kml style, Avenza kml style, brouter kml style, ogr2ogr kml style 
    # add extra codes to handle mapshaper kml    
        try:
            raw_array = (j.LineString.coordinates).text.split(' ') # raw, remove white spaces and \n
            try:
                label = str(j.name)
            except:
                label = ''
            try:
                time_str=str(j.TimeStamp.when)
            except:
                time_str=''

            if (len(raw_array)==1):  # mapshaper KML needs some extra processing
                raw_array[0].replace('\n',  " "  )
                temp_array = raw_array[0].split()
                raw_array = [f'{coord}' for coord in temp_array]

            array_1 = list( item.strip() for item in raw_array)
            array_2 = [ item for item in array_1 if item != ''] 
            #now we have a list of strings, e.g.  ['-123,49', '-123,49', '-123,49']
            #below is Method 1, very compact code, a bit too hard to read.
            ######  my_line_object=LineString( list(map(float, item.split(','))) for item in array_2  )    
            # we need a list of list of floats, using simpler code:
            # to produce this list of floats [[-123,49], [-123,49], [-123,49]] 
            magic=[]
            for item in array_2:
                float_values = [float(val) for val in item.split(',')]
                magic.append(float_values)
            my_line_object = LineString(magic)

            if (time_str == "none"):
                basket.append(Feature(geometry=my_line_object,properties={"name":label} ))
            else:
                basket.append(Feature(geometry=my_line_object,properties={"name":label,"timestamp":time_str} ))      
        except:
            pass

    for j in set_of_features:            
        try:
            coord_array = (j.Polygon.outerBoundaryIs.LinearRing.coordinates).text.split(' ')
            try:
                label = str(j.name)
            except:
                label = ''      
            my_poly = Polygon( [ [list(map(float, item.split(','))) for item in coord_array] ] )
            basket.append(Feature(geometry=my_poly,properties={"name":label}  ))  
        except:
            pass

# main()

print ("For simple kml files only. For more complex files, use 'ogr2ogr sample.geojson sample.kml' ")

if len(sys.argv) < 2:
    print("Enter a kml file to convert to GeoJSON ")
    sys.exit(1)

with open(sys.argv[1]+".kml") as f:
    root = parser.parse(f).getroot()

basket = []  # empty basket to hold/collect features

# kml comes in many different sizes and shapes and it gets out of control very quickly.
try:
    process_features(root.Document.Placemark) # minimalist KML
except:
    try:
        process_features(root.Document.Folder.Placemark) # Avenza KML export
    except:
        try:
            process_features(root.Document.Document.Placemark) # ogr2ogr "LIBKML" KML
        except:
            pass  # may come across other KML structures, add it here. If all else fails, use ogr2ogr

geojson_string = json.dumps(FeatureCollection(basket), indent=2, ensure_ascii=False)
print(geojson_string)

with open(sys.argv[1]+'.geojson', 'w') as outfile:
    outfile.write( geojson_string )

