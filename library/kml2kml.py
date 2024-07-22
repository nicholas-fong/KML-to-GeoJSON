from lxml import etree as ET
import xml.dom.minidom as minidom
import sys

kml_namespace = {'kml': 'http://www.opengis.net/kml/2.2'}

# style 1 of pretty print, eliminat blank lines, returns regular string
def prettify(element):
    rough_string = ET.tostring(element, encoding='utf-8', xml_declaration=True)
    reparsed = minidom.parseString(rough_string)
    pretty_string = (reparsed.toprettyxml(indent="  ", encoding='utf-8')).decode('utf-8')
    # Remove extra blank lines
    lines = [line for line in pretty_string.split('\n') if line.strip()]
    return '\n'.join(lines)
# style 2 of pretty print: ET.tosring --> minidom --> toprettyxml, returns binary string
# def prettify(element):
#   rough_string = ET.tostring(element, encoding='utf-8', xml_declaration=True)
#   reparsed = minidom.parseString(rough_string)
#   return reparsed.toprettyxml(indent="  ", encoding='utf-8')
# style 3 KML to string pretty print
# print( ET.tostring(kml, encoding='utf-8', pretty_print=True, xml_declaration=True ).decode() )

# main()
with open(sys.argv[1] + ".kml") as infile:
    tree = ET.parse(infile)
root = tree.getroot()

# sylte 1 output: <?xml version="1.0" encoding="utf-8"?>
pretty_kml = prettify(root)
#print (pretty_kml)
with open(sys.argv[1]+'.kml', 'w') as output_file:
    output_file.write(pretty_kml)
# style 2 output: <?xml version='1.0' encoding='UTF-8'?>
# Save the KML element
# tree.write(sys.argv[1] + ".kml", encoding="utf-8", xml_declaration=True)
