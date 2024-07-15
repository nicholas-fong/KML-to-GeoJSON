## Python snippets to convert between GPX, KML and GeoJSON.

KML to GeoJSON:<br>

Snippet to convert KML placemarks to GeoJSON's Point, LineString, Polygon and GeometryCollection. It also converts KML gx:Track to GeoJSON LineString. 
```
$python kml2geo.py
```

Snippet to convert GeoJSON to KML:
```
$python geo2kml.py
```

Online tool: https://geojson.io <br>

Some utilities to convert ascii file (e.g. sample.asc) to GeoJSON and GPX:

```
$python asc2geo.py sample
$python asc2wpt.py sample
$python asc2rte.py sample
$python asc2trk.py sample

```
A utility to calculate the distance between two geolocations using haversine distance formula:
```
$python distance.py
```
Conversions between GPX, GeoJSON and KML
```
$python gpx2geo.py grouse
$python geo2kml.py grouse
```
