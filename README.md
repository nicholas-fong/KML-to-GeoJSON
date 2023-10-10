## Python snippets to convert between KML and GeoJSON.

KML to GeoJSON:<br>

KML data structure can range from relatively straight forward to more complex gx prefix namespace extensions. This snippet convert simple KML placemarks to GeoJSON Point, LineString and Polygon. It can handle KML gx:Track as well. 

GeoJSON to KML and KML to GeoJSON:
```
$python3 kml2geo.py
$python3 geo2kml.py
```

KML to KML: regenerate a minimalist KML file without bells and whistles, gx:Track is not implemented.
```
$python3 kml2kml.py
```

For KML with more complex structure, use GDAL's org2ogr:
```
$sudo apt install gdal-bin
$ogr2ogr fountains.kml fountains.geojson
$ogr2ogr fountains.geojson fountains.kml
```
From asc file, create GeoJSON, gpx waypoint, gpx route, gpx track files (using sample.asc)
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
