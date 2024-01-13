# Convert GeoJSON Point, LineString, Polygon to kml Point, LineString, Polygon placemarks
# Convert GeoJSON MultiPoint to kml MultiGeometry Point placemark
# Convert GeoJSON MultiLineString to kml MultiGeometry LineString placemark
# Convert GeoJSON MultipPolygon to kml MultiGeometry Polygon placemark
# Convert GeoJSON GeometryCollection Point, LineString and Polygon to kml MultiGeometry placemark
# For more complex GeoJSON, use ogr2ogr outfile.kml infile.geojson (sudo apt install gdal-bin)

import json
import sys
from lxml import etree as ET     # pip install lxml

# Load GeoJSON data
with open( sys.argv[1]+'.geojson', 'r') as infile:
   data = json.load ( infile )

# Create a KML root element
kml = ET.Element('kml', xmlns='http://www.opengis.net/kml/2.2')

# A function to convert GeoJSON feature to KML placemark
def geojson_feature_to_kml(feature):
    placemark = ET.SubElement(kml, 'Placemark')

    property = feature.get('properties', None)
    if property is not None:
        # Extract the name
        name = feature['properties'].get('name', '') or feature['properties'].get('NAME', '') or feature['properties'].get('Name', '')
        if name:
            name_element = ET.SubElement(placemark, 'name')
            name_element.text = name
        # Extract properties description
        description = feature['properties'].get('description', None)
        if description:
            desc_element = ET.SubElement(placemark, 'description')
            desc_element.text = description
        # Extract timestamp
        timestamp = feature['properties'].get('timestamp', None)
        if timestamp is None:
            timestamp = feature['properties'].get('TimeStamp', None)
        if timestamp:
            timestamp_element = ET.SubElement(placemark, 'TimeStamp')
            when_element = ET.SubElement(timestamp_element, 'when')
            when_element.text = timestamp

    if feature['geometry']['type'] == 'Point':
        point = ET.SubElement(placemark, 'Point')
        coordinates = ET.SubElement(point, 'coordinates')
        coordinates.text = ','.join(map(str, feature['geometry']['coordinates']))
    if  feature['geometry']['type'] == 'MultiPoint':
        multigeometry = ET.SubElement(placemark, 'MultiGeometry')
        for each_point in feature['geometry']['coordinates']:
            point = ET.SubElement(multigeometry, 'Point')
            coordinates = ET.SubElement(point, 'coordinates')
            for item in each_point:
                coordinates.text =  ','.join(map(str,each_point))
    if feature['geometry']['type'] == 'LineString':
        linestring = ET.SubElement(placemark, 'LineString')
        coordinates = ET.SubElement(linestring, 'coordinates')
        coordinates.text = ' '.join(','.join(map(str, coords)) for coords in feature['geometry']['coordinates'])
    if feature['geometry']['type'] == 'MultiLineString':
        multigeometry = ET.SubElement(placemark, 'MultiGeometry')
        for each_line in feature['geometry']['coordinates']:
            linestring = ET.SubElement(multigeometry, 'LineString')
            coordinates = ET.SubElement(linestring, 'coordinates')
            coordinates.text = ' '.join(','.join(map(str, coords)) for coords in each_line)
    if feature['geometry']['type'] == 'Polygon':
        polygon = ET.SubElement(placemark, 'Polygon')
        outer = ET.SubElement(polygon, 'outerBoundaryIs')
        linear_ring = ET.SubElement(outer, 'LinearRing')
        coordinates = ET.SubElement(linear_ring, 'coordinates')
        coordinates.text = ' '.join(','.join(map(str, coords)) for coords in feature['geometry']['coordinates'][0])
        for inner_ring_coords in feature['geometry']['coordinates'][1:]:
            inner = ET.SubElement(polygon, 'innerBoundaryIs')
            inner_ring = ET.SubElement(inner, 'LinearRing')
            inner_coordinates = ET.SubElement(inner_ring, 'coordinates')
            inner_coordinates.text = ' '.join(','.join(map(str, coords)) for coords in inner_ring_coords)
    if feature['geometry']['type'] == 'MultiPolygon':
        multigeometry = ET.SubElement(placemark, 'MultiGeometry')
        for item in feature['geometry']['coordinates']:
            polygon = ET.SubElement(multigeometry, 'Polygon')
            outer = ET.SubElement(polygon, 'outerBoundaryIs')
            linear_ring = ET.SubElement(outer, 'LinearRing')
            coordinates = ET.SubElement(linear_ring, 'coordinates')
            coordinates.text = ' '.join(','.join(map(str, coords)) for coords in item[0] )
            for inner_ring_coords in item[1:]:
                inner = ET.SubElement(polygon, 'innerBoundaryIs')
                inner_ring = ET.SubElement(inner, 'LinearRing')
                inner_coordinates = ET.SubElement(inner_ring, 'coordinates')
                inner_coordinates.text = ' '.join(','.join(map(str, coords)) for coords in inner_ring_coords)
    if feature['geometry']['type'] == 'GeometryCollection':
        ET.SubElement(placemark, 'MultiGeometry')            
        for item in feature['geometry']['geometries']:
            if item['type']=='Point':
                point = ET.SubElement(placemark, 'Point')
                coordinates = ET.SubElement(point, 'coordinates')
                coordinates.text = ','.join(map(str, item['coordinates']))
            if item['type']=='LineString':
                linestring = ET.SubElement(placemark, 'LineString')
                coordinates = ET.SubElement(linestring, 'coordinates')
                coordinates.text = ' '.join(','.join(map(str, coords)) for coords in item['coordinates']) 
            if item['type']=='Polygon':
                polygon = ET.SubElement(placemark, 'Polygon')
                outer = ET.SubElement(polygon, 'outerBoundaryIs')
                linear_ring = ET.SubElement(outer, 'LinearRing')
                coordinates = ET.SubElement(linear_ring, 'coordinates')
                coordinates.text = ' '.join(','.join(map(str, coords)) for coords in item['coordinates'][0])
                for inner_ring_coords in item['coordinates'][1:]:
                    inner = ET.SubElement(polygon, 'innerBoundaryIs')
                    inner_ring = ET.SubElement(inner, 'LinearRing')
                    inner_coordinates = ET.SubElement(inner_ring, 'coordinates')
                    inner_coordinates.text = ' '.join(','.join(map(str, coords)) for coords in inner_ring_coords)

# Iterate through GeoJSON features and create KML placemark for each feature
for feature in data['features']:
    geojson_feature_to_kml(feature)

# Convert binary KML object to a string
kml_string = ET.tostring(kml, encoding='UTF-8', pretty_print=True, xml_declaration=True ).decode()

#print(kml_string)
with open(sys.argv[1]+'.kml', 'w') as output_file:
    output_file.write(kml_string)
