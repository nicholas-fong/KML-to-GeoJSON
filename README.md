## gpx-add-SRTM-elevation
Adding SRTM elevation points to a gpx file

Building on top of [SRTM-GeoTIFF](https://github.com/nicholas-fong/SRTM-GeoTIFF), this Python code takes a gpx file and matches up SRTM-GeoTIFF data stored on local drive and outputs to STDOUT.

Kowloon Peak is one of many hiking destinations in Hong Kong
```
$python gpx-add-elevation.py Kowloon-Peak
$Python gpx-add-elevation.py Kowloon-Peak > Kowloon-Peak-elevation.gpx
```

You can achieve the same with online tool [GPS Visualizer](https://www.gpsvisualizer.com/).

This Python code offers an offline solution. If you have recorded gpx tracks using mobile phones, you can use this code to clean up/smooth the elelvation profile of the gpx tracks. 

[How to download USGS-SRTM GeoTIFF tiles](/EarthExplorer-howto.md)
