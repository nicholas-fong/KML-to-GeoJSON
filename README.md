Python snippets to convert between KML and GeoJSON

KML data structure can range from relatively simple to complex. This snippet can convert simple KML placemark to GeoJSON Points, LineStrings and Polygons. For complex KML files, use GDAL's ogr2ogr to do the conversion.

For the GeoJSON to KML converter, geopandas is not used. Only geojson and simplekml modules are used. This increases the speed.
