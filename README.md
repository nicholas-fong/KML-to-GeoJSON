Python snippets to convert between KML and GeoJSON.

KML to GeoJSON:<br>

KML data structure can range from relatively straight forward to complex gx prefix namespace extensions. This snippet convert simple KML (without gx prefix namespace extensions) placemarks to GeoJSON Point, LineString and Polygon. 

GeoJSON to KML and vice versa:
```
$python3 geo2kml.py
$python3 kml2geo.py
```

GeoJSON to KML and KML to GeoJSON, using GDAL's org2ogr:<br>
(can be used to handle more complex gx prefix namespace extensions)
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