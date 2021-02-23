## gpx-add-SRTM
A snippet to append or update SRTM elevation points to waypoints, routes and tracks of a gpx file.

Based on [SRTM-GeoTIFF](https://github.com/nicholas-fong/SRTM-GeoTIFF), this Python snippet takes a gpx file and matches up SRTM data stored on local drive and outputs to stdout.

### Example
(Grouse Grind is a popular hiking trail in Vancouver, Canada)
```
$python gpx-add-elevation.py grouse-grind
$Python gpx-add-elevation.py grouse-grind > grouse-grind-elevation.gpx
```

You can achieve the same with an online tool [GPS Visualizer](https://www.gpsvisualizer.com/).

This Python snippet offers an offline solution if the online tool does not cover your area of interest. 

If you have recorded gpx tracks using mobile phones, you can use this snippet to clean up/smooth out the elelvation profile. For example, if you recroded a gpx track walking on a beach, it is not uncommon to see the elevation profile shows you ocassionally walked under water. This Python snippet with appropriate STRM file (GeoTIFF) will clean it up.
