Python snippets to convert between KML and GeoJSON.

KML to GeoJSON:<br>
KML data structure can range from relatively straight forward to complex schema generated. This snippet can convert simple KML placemarks to GeoJSON Point, LineString and Polygon features. For more complex KML files, use GDAL's ogr2ogr to do the initial conversion on a Linux machine.

GeoJSON to KML:
```
python3 geo2kml.py
python2 kml2geo.py
```

Using GDAL's ogr2ogr to do KML / GeoJSON conversions: <br>
install gdal-bin: 
```
sudo apt install gdal-bin
```
GeoJSON to KML conversion
```
ogr2ogr -f 'KML' -a_srs EPSG:4326 fountains.kml fountains.geojson
or
ogr2ogr -f 'LIBKML' foundtains.kml fountains.geojson
or
ogr2ogr fountains.kml fountains.geojson
```
KML to GeoJSON conversion
```
ogr2ogr fountains.geojson fountains.kml
```
GPX to KML conversion
```
ogr2ogr -f 'LIBKML' -mapFieldType DateTime=String fountains.kml fountains.gpx
(result is not very satisfactory, elevations in kml are lost)


```
