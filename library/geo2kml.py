import sys
import geojson
import simplekml

# minimalist GeoJSON to KML converter

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
            myline.coords = coordinates

        if geometry_type == 'Polygon':
            mypoly = kml.newpolygon()
            mypoly.name = properties.get('name') or properties.get('Name') or properties.get('NAME')
            mypoly.outerboundaryis = coordinates[0]
            # Polygon: first element of a list of lists of list is the Polygon outer ring coordinates
            # simplekml only supports one inner ring, hence decide to not implement inner rings

#print(kml.kml())
kml.save(sys.argv[1]+".kml")

