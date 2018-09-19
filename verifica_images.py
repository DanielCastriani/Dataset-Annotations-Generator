#pylint: disable=E1101

import os
import sys
import matplotlib.pyplot as plt
import cv2
from matplotlib.widgets import RectangleSelector
import xml_writer as w_xml
import class_counter as c_count
import numpy as np
import xml.etree.ElementTree as ET

exts = ['png','PNG','jpg','JPG']
colors = [tuple([0,255,0]),tuple([0,255,255]),tuple([0,0,255]),tuple([255,0,0]),tuple([255,255,255]),tuple([255,126,0])]

image_folder = 'images'
xml_folder = 'annotations'
trash_dir = 'trash'

trash_xml = os.path.join(trash_dir,xml_folder)
trash_img = os.path.join(trash_dir,image_folder)

img_file = ""
xml_file = ""

skp = 0
qtd = 0

def onkeypress(event):
    global img_file,xml_file
    if event.key == 'q':
        exit()
    elif event.key == ' ':
        plt.close()
    elif event.key == 'f1':        
        os.system('mv {old} {new}'.format(old = xml_file,new = trash_xml))
        os.system('mv {old} {new}'.format(old = img_file.path,new = trash_img))

        plt.close()

def getCor(label):
    if label == "regulamentacao":
        return colors[0]
    elif label == "advertencia":
        return colors[1]
    elif label == "pare":
        return colors[2]
    elif label == "de_preferencia":
        return colors[3]
    elif label == "marcador_alimnhamento":
        return colors[4]
    elif label == "marcador_de_perigo":
        return colors[5]


def exibe_bound_box(image,xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        lb = obj.find('name').text            
        bb = obj.find('bndbox')
        tl = (int(bb.find('xmin').text), int(bb.find('ymin').text))
        br = int(bb.find('xmax').text), int(bb.find('ymax').text)

        cor = getCor(lb)
        image = cv2.rectangle(image, tl, br, cor, 3)
        image = cv2.putText(image, lb, tl, cv2.FONT_HERSHEY_COMPLEX, 1, cor, 2)

    return image

def legenda():
    os.system('clear')

    print('_________________________________________________________________')
    print('[Space] - Proxima imagem')
    print('[f1] - Mover para a pasta trash')
    _,_,msg = c_count.count()
    print('_________________________________________________________________')
    print(msg)
    print('_________________________________________________________________')
    print('N: ',qtd)

def order_by(elm):
    return elm[1].name
    
if __name__ == '__main__':

    for i in range(0,len(sys.argv)):
        if sys.argv[i].startswith('n='):
            try:
                skp = int(sys.argv[i].split('=')[-1])
                qtd = skp
            except ValueError as ex:
                print('O parametro está incorreto')
                print("\tn=[num]\t pula [num] arquivo(s)")
                exit()      

    if not os.path.isdir(trash_dir):
        os.mkdir(trash_dir)

    if not os.path.isdir(trash_xml):
        os.mkdir(trash_xml)

    if not os.path.isdir(trash_img):
        os.mkdir(trash_img)

    if not os.path.isdir(image_folder) or not os.path.isdir(xml_folder):
        print('Não contem dados')
        exit()

    legenda()
    
    all_files = sorted(enumerate(os.scandir(image_folder)),key=order_by)

    for n,image_fl in all_files:   
        img_file = image_fl
        verifica_existe = False     
        xml_file = ""

        for ext in exts:      
            xml_file = os.path.join(xml_folder,img_file.name.replace(ext,'xml'))      
            if os.path.exists(xml_file):
                verifica_existe = True
                break

        if verifica_existe is False:
            continue

        if skp > 0:
            skp -= 1
            continue
        
        qtd += 1
        with open('log.txt','w') as f_log:
            f_log.write(str(qtd) + "\n")
            
        
        print('File:['+str(n)+'] - '+img_file.name)

        fig, ax = plt.subplots(1)        

        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()
        
        image = cv2.imread(img_file.path)
        image = exibe_bound_box(image,xml_file)
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        ax.imshow(image)

        key = plt.connect('key_press_event',onkeypress)
        plt.show()

        legenda()