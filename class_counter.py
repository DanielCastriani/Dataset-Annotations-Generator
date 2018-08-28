import xml.etree.ElementTree as ET
import os
dir = 'annotations'

cl = []
qtd = []

def find(p):
    global cl
    global qtd

    for obj in p.iter('object'):
        for name in obj.iter('name'):
            if name.text in cl:
                index = cl.index(name.text)
                qtd[index] += 1
            else:
                cl.append(name.text)
                qtd.append(1)


for n, f_xml in enumerate(os.scandir(dir)):
    if f_xml.name.endswith('xml') == True:
        tree = ET.parse(f_xml)
        root = tree.getroot()
        find(root)       

for i in range(len(qtd)):
    print(cl[i],'',qtd[i])