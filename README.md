## Python snippets to convert between KML and GeoJSON.

KML to GeoJSON:<br>

KML data structure can range from relatively straight forward to complex gx prefix namespace extensions. This snippet convert simple KML (without gx prefix namespace extensions) placemarks to GeoJSON Point, LineString and Polygon. 

GeoJSON to KML and KML to GeoJSON:
```
$python3 kml2geo.py
$python3 geo2kml.py
```

KML to KML: regenerate a minimalist KML file without bells and whistles:
```
$python3 kml2kml.py
```

KML with more complex gx prefix namespace, use GDAL's org2ogr:
```
$sudo apt install gdal-bin
$ogr2ogr fountains.kml fountains.geojson
$ogr2ogr fountains.geojson fountains.kml
```
From asc file, create GeoJSON and KML (using sample.asc)
```
$python3 asc2geokml.py sample
```
Calculate distance between two geolocations using haversine distance formula
```
$python3 distance.py
```
From GPX to GeoJSON and KML (in that order):
```
$python3 gpx2geo.py grouse
$python3 geo2kml.py grouse
```
