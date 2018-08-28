#pylint: disable=E1101
import os
import cv2
from lxml import etree
import xml.etree.cElementTree as ET

def write_xml(folder,img,objects,tl,br,savedir):
    '''
    folder = pasta da imagem

    img = path do arquivo

    objects = label do objeto

    tl = (x1,y1)   top left

    br = (x2,y2)    botton right

    '''
    if len(objects) == 0:
        print('Não criou arquivo')
        return False

    if not os.path.isdir(savedir):
        os.mkdir(savedir)
    
    image = cv2.imread(img.path)
    height,width,depth = image.shape

    annotation = ET.Element('annotation')# main tag
    ET.SubElement(annotation,'folder').text = folder
    ET.SubElement(annotation,'filename').text = img.name
    # Não vai adicionar nem tag source e nem owner
    ET.SubElement(annotation,'segmented').text = 0

    size = ET.SubElement(annotation,'size')
    ET.SubElement(size,'width').text = str(width)
    ET.SubElement(size,'height').text = str(height)
    ET.SubElement(size,'depth').text = str(depth)

    for obj, topl,botr in zip(objects,tl,br):
        ob = ET.SubElement(annotation,'object')
        ET.SubElement(ob,'name').text = obj
        ET.SubElement(ob,'pose').text = 'Unspecified'
        ET.SubElement(ob,'truncated').text = '0'
        ET.SubElement(ob,'difficult').text = '0'

        bbox = ET.SubElement(ob,'bndbox')
        ET.SubElement(bbox,'xmin').text = str(topl[0])
        ET.SubElement(bbox,'ymin').text = str(topl[1])
        ET.SubElement(bbox,'xmax').text = str(botr[0])
        ET.SubElement(bbox,'ymax').text = str(botr[1])

    xml_str = ET.tostring(annotation)
    root = etree.fromstring(xml_str)
    xml_str = etree.tostring(root,pretty_print=True)

    save_path = os.path.join(savedir,img.name.replace('png','xml'))
    with open(save_path,'wb') as temp_xml:
        temp_xml.write(xml_str)
    print('\nXML Gerado {} objetos\n'.format(str(len(objects))))

    return True