## Python snippets to convert between GPX, KML and GeoJSON.

KML to GeoJSON:<br>

Snippet to convert KML placemarks to GeoJSON's Point, LineString, Polygon and GeometryCollection. It also converts KML gx:Track to GeoJSON LineString. 
```
$python3 kml2geo.py
```

Snippet to convert GeoJSON to KML:
```
$python3 geo2kml.py
```

Online tool: https://geojson.io <br>

Some utilities to convert ascii file to GeoJSON and GPX:

```
$python3 asc2geo.py sample
$python3 asc2wpt.py sample
$python3 asc2rte.py sample
$python3 asc2trk.py sample

```
A utility to calculate the distance between two geolocations using haversine distance formula:
```
$python3 distance.py
```
Conversions between GPX, GeoJSON and KML
```
$python3 gpx2geo.py grouse
$python3 geo2kml.py grouse
```
