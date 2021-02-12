# gpx-add-SRTM-elevation
Add SRTM elevation points to a gpx file

Building on top of project [SRTM-GeoTIFF](https://github.com/nicholas-fong/SRTM-GeoTIFF), this Python code takes a gpx file and matches up SRTM data files (GeoTIFF) stored on local drive and outputs to STDOUT.

Example Usage:

download n22_e114.tif, Kowloon-Peak.gpx and gpx-add-elevation.py to a local directory,

python gpx-add-elevation.py Kowloon-Peak

See SRTM-GeoTIFF on how to find and download USGS-SRTM GeoTIFF files.

You can achieve the same with [GPS Visualizer](https://www.gpsvisualizer.com/).

This python code offers an offline solution and the dataset is from SRTM.
