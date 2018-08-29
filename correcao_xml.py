'<segmented>0</segmented>'

import os
import xml.etree.ElementTree as ET
from lxml import etree

if os.path.exists('correcao_xml') == False:
    os.mkdir('correcao_xml')

for n,xml_file in enumerate(os.scandir('annotations')):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    xml_str = ET.tostring(root)
    r = etree.fromstring(xml_str)
    xml_str = etree.tostring(r,pretty_print=True)

    xml_str = xml_str.decode('utf-8')
    if '<segmented>0</segmented>' not in xml_str:
        xml_str = xml_str.replace('<segmented/>','<segmented>0</segmented>')
    else:
        continue
        
    xml_str = xml_str.encode('utf-8')

    nf = os.path.join('correcao_xml',xml_file.name)
    with open(nf,'wb') as temp_xml:
        temp_xml.write(xml_str)

    print(xml_file)