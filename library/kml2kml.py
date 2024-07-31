from lxml import etree as ET
import xml.dom.minidom as minidom
import sys

kml_namespace = {'kml': 'http://www.opengis.net/kml/2.2'}

def prettify(element):
    rough_string = ET.tostring(element, encoding='utf-8', xml_declaration=True)
    reparsed = minidom.parseString(rough_string)
    pretty_string = (reparsed.toprettyxml(indent="  ", encoding='utf-8')).decode('utf-8')
    # Remove extra blank lines
    lines = [line for line in pretty_string.split('\n') if line.strip()]
    return '\n'.join(lines)

with open(sys.argv[1] + ".kml") as infile:
    tree = ET.parse(infile)
root = tree.getroot()

pretty_kml = prettify(root)
with open(sys.argv[1]+'.kml', 'w') as outfile:
    outfile.write(pretty_kml)
print ( f"File saved as {sys.argv[1]+'kml'}")    