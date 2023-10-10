import xml.etree.ElementTree as ET
import sys
import simplekml
kml = simplekml.Kml()
kml_namespace = {'kml': 'http://www.opengis.net/kml/2.2'} 
# Define namespaces (KML uses namespaces)

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
# Open the KML file
with open(sys.argv[1]+".kml") as infile:
    tree = ET.parse(infile)
root = tree.getroot()
infile.close()  #for peace of mind

# Iterate through Placemark elements
for placemark in root.findall('.//kml:Placemark', namespaces=kml_namespace):
    name_elem = placemark.find('kml:name', namespaces=kml_namespace)
    name = name_elem.text.strip() if name_elem is not None else 'Unnamed'

    # Check for geometry types: Point, LineString, or Polygon
    point = placemark.find('.//kml:Point', namespaces=kml_namespace)
    line_string = placemark.find('.//kml:LineString', namespaces=kml_namespace)
    polygon = placemark.find('.//kml:Polygon', namespaces=kml_namespace)

    if point is not None:
        mypoint = kml.newpoint(name=name)
        mypoint.coords = extract_coordinates(point)

    elif line_string is not None:
        myline = kml.newlinestring(name=name)
        myline.coords = extract_coordinates(line_string)

    elif polygon is not None:
        mypol = kml.newpolygon(name=name)
        outer_ring = polygon.find('.//kml:outerBoundaryIs/kml:LinearRing', namespaces=kml_namespace)
        mypol.outerboundaryis = extract_coordinates(outer_ring) 
        # "simplekml" can create only one interior ring inside an exterior ring.
        inner_rings = polygon.findall('.//kml:innerBoundaryIs/kml:LinearRing', namespaces=kml_namespace)
        for inner_ring in inner_rings:                
            mypol.innerboundaryis = extract_coordinates(inner_ring)

#print(kml.kml())
kml.save(sys.argv[1]+".kml")
