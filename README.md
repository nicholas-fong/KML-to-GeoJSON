## gpx-add-SRTM-elevation
Append or update SRTM elevation points to waypoints, routes and tracks of gpx file.

Build on top of [SRTM-GeoTIFF](https://github.com/nicholas-fong/SRTM-GeoTIFF), this Python module takes a gpx file and matches up SRTM data (GeoTIFF) stored on local drive and outputs to stdout.

### Example
(Kowloon Peak is one of many hiking destinations in Hong Kong)
```
$python gpx-add-elevation.py Kowloon-Peak
$Python gpx-add-elevation.py Kowloon-Peak > Kowloon-Peak-elevation.gpx
```

You can achieve the same with an online tool [GPS Visualizer](https://www.gpsvisualizer.com/).

This Python module offers an offline solution if the online tool does not cover your area of interest. If you have recorded gpx tracks using mobile phones, you can use this module to clean up/smooth out the elelvation profile. For example, if you recroded a gpx track walking on a beach, it is not uncommon to see the elevation profile shows you ocassionally walked under water. This Python module willl clean it up.

[Earth Explorer primer](https://github.com/nicholas-fong/SRTM-GeoTIFF/blob/main/EarthExplorer.md)
