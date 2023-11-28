import sys
import xml.etree.ElementTree as ET
from geojson import FeatureCollection, Feature, Point, LineString, Polygon, dumps

# Define namespaces (KML uses kml namespaces and gx namespaces)
kml_namespace = {'kml': 'http://www.opengis.net/kml/2.2'} 
gx_namespace =  {'gx': 'http://www.google.com/kml/ext/2.2'}

basket=[]

# function to extract coordinates from a geometry element, returns an array of tuples
def extract_coordinates(geometry_element):
    coordinates_elem = geometry_element.find('kml:coordinates', namespaces=kml_namespace)
    if coordinates_elem is not None:
        # coordinates is a list of strings
        coordinates = coordinates_elem.text.strip().split()
        # convert to a list of tuples
        list_of_tuples = [tuple(map(float, item.split(','))) for item in coordinates]
        return list_of_tuples

# main()
# For more complex KML files, use GDAL's 'ogr2ogr' : sudo apt install gdal-bin

with open(sys.argv[1]+".kml") as infile:
    tree = ET.parse(infile)
root = tree.getroot()

# Iterate through Placemark elements
for placemark in root.findall('.//kml:Placemark', namespaces=kml_namespace):
    name_elem = placemark.find('kml:name', namespaces=kml_namespace)
    name = name_elem.text.strip() if name_elem is not None else 'Unnamed'
    time_elem = placemark.find('.//kml:TimeStamp/kml:when', namespaces=kml_namespace)
    time_stamp = time_elem.text.strip() if time_elem is not None else None

    # Check for geometry types: Point, LineString, or Polygon
    point = placemark.find('.//kml:Point', namespaces=kml_namespace)
    line_string = placemark.find('.//kml:LineString', namespaces=kml_namespace)
    polygon = placemark.find('.//kml:Polygon', namespaces=kml_namespace)

    if point:
        my_point = extract_coordinates(point)
        basket.append(Feature(geometry=Point(my_point[0]), properties={"name":name}))

    elif line_string:
        my_line = extract_coordinates(line_string)
        basket.append(Feature(geometry=LineString(my_line),properties={"name":name,"timestamp":time_stamp} )) 

    elif polygon:
        all_rings = []
        outer_ring = polygon.find('.//kml:outerBoundaryIs/kml:LinearRing', namespaces=kml_namespace)
        all_rings.append(extract_coordinates(outer_ring))
        
        inner_rings = polygon.findall('.//kml:innerBoundaryIs/kml:LinearRing', namespaces=kml_namespace)
        for inner_ring_elem in inner_rings:                
            all_rings.append(extract_coordinates(inner_ring_elem))
        basket.append(Feature(geometry=Polygon(all_rings),properties={"name":name})) 

    # Look for <gx:Track> <gx:coord>
    gx_track = placemark.find("{http://www.google.com/kml/ext/2.2}Track")
    if gx_track is not None:
        gx_coord = gx_track.findall("{http://www.google.com/kml/ext/2.2}coord")  #<gx:coord>
        list_coords=[]
        for coord in gx_coord:
            my_xyz = list(map(float, coord.text.split()))  # coord is a list of 3 floats: longitude, latitude, altitude
            list_coords.append(my_xyz)  # collect all the track points
        list_tuples = [tuple(lst) for lst in list_coords]  # convert list of xyz to list of tuples before invoking constructor    
        basket.append(Feature(geometry=LineString(list_tuples),properties={"name":name,"timestamp":time_stamp} ))

geojson_string = dumps(FeatureCollection(basket), indent=2, ensure_ascii=False)
# defaults to multi-line human-readable geojson output
# comment out above line, uncomment below line to do one-line geojson output, to save space.
# geojson_string = dumps(FeatureCollection(basket), ensure_ascii=False)

print(geojson_string)
with open(sys.argv[1]+'.geojson', 'w') as outfile:
    outfile.write( geojson_string )
