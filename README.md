Python snippets to convert between KML and GeoJSON.

KML to GeoJSON:<br>
KML data structure can range from relatively straight forward to complex schema-generated extensions. This snippet can convert simple KML placemarks to GeoJSON Point, LineString and Polygon features. 


GeoJSON to KML and vice versa:
```
$python3 geo2kml.py
$python3 kml2geo.py
```

GeoJSON to KML and vice versa, using GDAL's org2ogr:<br>
(typically used to handle more complex data sets)
```
$sudo apt install gdal-bin

$ogr2ogr -f 'LIBKML' -a_srs EPSG:4326 fountains.kml fountains.geojson
$ogr2ogr -f 'LIBKML' foundtains.kml fountains.geojson

$ogr2ogr fountains.geojson fountains.kml
```
From asc to GeoJSON and KML (see sample.asc)
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