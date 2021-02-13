# gpx-add-SRTM-elevation
Adding SRTM elevation points to a gpx file

Building on top of [SRTM-GeoTIFF](https://github.com/nicholas-fong/SRTM-GeoTIFF), this Python code takes a gpx file and matches up SRTM data files (GeoTIFF) stored on local drive and outputs to STDOUT.

Example Usage:<br>
download n22_e114.tif, Kowloon-Peak.gpx and gpx-add-elevation.py to a local directory,<br>
python gpx-add-elevation.py Kowloon-Peak

[How to download USGS-SRTM GeoTIFF files](https://github.com/nicholas-fong/gpx-add-SRTM-elevation/blob/main/EarthExplorer-howto.md)

You can achieve the same with online tool [GPS Visualizer](https://www.gpsvisualizer.com/).

This python code offers an offline solution and the dataset is from SRTM. If you have a recorded gpx track from mobile phone, you can use this code to cllean/imporve the elelvation profile of the gpx track (more accurate and generally smoother). 
