Python snippets to convert between KML and GeoJSON.

KML to GeoJSON:<br>
KML data structure can range from relatively straight forward to complex schema generated. This snippet can convert simple KML placemarks to GeoJSON Point, LineString and Polygon features. For more complex KML files, use GDAL's ogr2ogr to do the initial conversion on a Linux machine.

GeoJSON to KML:<br>
Popular geopandas module is not deployed. Only geojson and simplekml modules are deployed.
