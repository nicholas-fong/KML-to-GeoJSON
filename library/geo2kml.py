import sys
import geojson
import simplekml

# this script does not use geopandas module hence it runs faster

if len(sys.argv) < 2:
    print("Please enter a geojson file to convert to kml ")
    sys.exit(1)

data = geojson.load(open( sys.argv[1] + '.geojson'))
kml = simplekml.Kml()

for i in range(len(data['features'])):
    try:
        myname = data['features'][i]['properties']['name']
    except:
        try:
            myname = data['features'][i]['properties']['Name']
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
        mypoly.outerboundaryis = geom['coordinates'][0] #first element of list of list is still a list

print(kml.kml())
kml.save(sys.argv[1]+".kml")