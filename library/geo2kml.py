import sys
import geojson
import simplekml

# minimalist GeoJSON to KML converter

user_input = input ("Lossy conversion: this converts Polygon's multiple interior rings to only one interior ring, proceed Y or N? ").strip().upper()

if user_input == 'Y':

    with open( sys.argv[1]+'.geojson', 'r') as infile:
        data = geojson.load ( infile )

    kml = simplekml.Kml()

    if 'features' in data:
        features = data['features']
        
        for feature in features:
            geometry_type = feature['geometry'].get('type', None)
            coordinates = feature['geometry'].get('coordinates', None)
            properties = feature.get('properties', None)

            if geometry_type == 'Point':
                mypoint = kml.newpoint()
                mypoint.name = properties.get('name') or properties.get('Name') or properties.get('NAME')
                mypoint.coords = [coordinates]

            if geometry_type == 'LineString':
                myline =  kml.newlinestring()
                myline.name = properties.get('name') or properties.get('Name') or properties.get('NAME')
                myline.timestamp.when = properties.get('timestamp') or properties.get('Timestamp') or properties.get('TimeStamp')
                tuples = list(map(tuple, coordinates))
                myline.coords = tuples

            if geometry_type == 'Polygon':
                mypoly = kml.newpolygon()
                mypoly.name = properties.get('name') or properties.get('Name') or properties.get('NAME')
                tuples = [[tuple(inner_lst) for inner_lst in outer_lst] for outer_lst in coordinates]
                i=0
                while i < len(coordinates):
                    if i==0:
                        mypoly.outerboundaryis = tuples[i]
                    else:
                        mypoly.innerboundaryis = tuples[i]
                    i+=1        
                # Polygon: first element of a list of lists of list is the Polygon's outer ring coordinates
                # simplekml only supports one inner ring, hence the last inner ring becomes the one and only inner ring.
                # this is a lossy conversion, unfortunately.
                # use this converter with caution

    print(kml.kml())
    kml.save(sys.argv[1]+".kml")

else:
    print("program aborted")
    sys.exit()
