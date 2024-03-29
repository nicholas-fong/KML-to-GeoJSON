## Python snippets to convert between KML and GeoJSON.

KML to GeoJSON:<br>

These snippets convert KML placemarks to GeoJSON's Point, LineString, Polygon and GeometryCollection. It can parse KML gx:Track to GeoJSON LineString. 

GeoJSON to KML and KML to GeoJSON:
```
$python3 kml2geo.py
$python3 geo2kml.py
```

For KML with more complex structure, use GDAL's org2ogr or oneline at geojson.io:
```
$sudo apt install gdal-bin
$ogr2ogr fountains.kml fountains.geojson
$ogr2ogr fountains.geojson fountains.kml
```
From ascii file, create GeoJSON, gpx waypoint, gpx route, gpx track files (see sample.asc)
```
$python3 asc2geo.py sample
$python3 asc2wpt.py sample
$python3 asc2rte.py sample
$python3 asc2trk.py sample

```
Calculate the distance between two geolocations using haversine distance formula
```
$python3 distance.py
```
From GPX to GeoJSON and then to KML (in that order):
```
$python3 gpx2geo.py grouse
$python3 geo2kml.py grouse
```
