Python snippets to convert between KML and GeoJSON.

KML to GeoJSON:<br>
KML data structure can range from relatively straight forward to complex schema generated extensions. This snippet can convert simple KML placemarks to GeoJSON Point, LineString and Polygon features. For more complex KML files, use GDAL's ogr2ogr to do the initial conversion on a Linux machine.

GeoJSON to KML and vice versa:
```
$python3 geo2kml.py
$python3 kml2geo.py
```

GeoJSON to KML and vice versa, using GDAL's org2ogr:
```
$sudo apt install gdal-bin
$python3 ogr2ogr -f 'KML' -a_srs EPSG:4326 fountains.kml fountains.geojson
$ogr2ogr -f 'LIBKML' foundtains.kml fountains.geojson
$ogr2ogr fountains.kml fountains.geojson
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
From GPX to GeoJSON and KML:
```
$python3 gpx2geo.py grouse
$python3 geo2kml.py grouse
```