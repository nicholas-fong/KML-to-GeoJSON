import sys
import geojson
import simplekml

# this script does not use geopandas module hence it runs faster

if len(sys.argv) < 2:
    print("Please enter a geojson file to convert to kml ")
    sys.exit(1)

with open( sys.argv[1]+'.geojson', 'r') as infile:
   data = geojson.load ( infile )

kml = simplekml.Kml()

for i in range(len(data['features'])):
    try:
        myname = data['features'][i]['properties']['name']
    except:
        try:
            myname = data['features'][i]['properties']['Name']
        except:
            try:
                myname = data['features'][i]['properties']['NAME']
            except:    
                myname = 'noname'

    geom = data['features'][i]['geometry']

    if geom['type'] == 'Point':
        mypoint = kml.newpoint(name=myname)
        mypoint.coords = [geom['coordinates']]

    elif geom['type'] == 'LineString':
        myline = kml.newlinestring(name=myname)
        myline.coords = geom['coordinates']

    elif geom['type'] == 'Polygon':
        mypoly = kml.newpolygon(name=myname)
        mypoly.outerboundaryis = geom['coordinates'][0] 
        # Polygon: first element of a list of lists is the list of Polygon outer ring coordinates

print(kml.kml())
kml.save(sys.argv[1]+".kml")
