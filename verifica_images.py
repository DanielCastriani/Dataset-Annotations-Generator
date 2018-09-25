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
import Util

exts = ['png','PNG','jpg','JPG']

image_folder = 'images'
xml_folder = 'annotations'
trash_dir = 'trash'

trash_xml = os.path.join(trash_dir,xml_folder)
trash_img = os.path.join(trash_dir,image_folder)

img_file = ""
xml_file = ""

skp = 0
qtd = 1
fig = None

def onkeypress(event):
    global img_file,xml_file
    global qtd
    if event.key == 'q':
        exit()
    elif event.key == ' ':
        plt.close()
    elif event.key == 'f1':        
        os.system('mv {old} {new}'.format(old = xml_file,new = trash_xml))
        os.system('mv {old} {new}'.format(old = img_file.path,new = trash_img))
        qtd -= 1
        plt.close()
    elif event.key == 'f5':        
        os.system('mv {old} {new}'.format(old = xml_file,new = trash_xml))
        qtd -=1
        plt.close()
    elif event.key == 'enter':
        Util.exibe_imagem(img_file,xml_file,ax,fig)
 

def legenda():
    Util.hb1()
    print('[Space] - Proxima imagem')
    print('[F1] - Mover imagem e xml para a pasta trash')
    print('[F5] - Mover xml para a pasta trash')
    print('[Enter] - Recarregar imagem')
    Util.plt_legenda()
    print('[Q] - Sair')
    _,_,qtd_arqs,msg = c_count.count()
    Util.hb1()
    print(msg)
    Util.hb1()
    print('N: ',qtd, '/',qtd_arqs)

def help():    
    print('Parametros')
    print("\t-h \thelp")
    print("\t-l \tultimo (arquivo log_verifica.txt)")
    print("\tn=[num]\t pula [num] arquivo(s)")

def order_by(elm):
    return elm[1].name
    
if __name__ == '__main__':
    os.system('clear')

    if len(sys.argv) == 1:
        help()

    for i in range(1,len(sys.argv)):
        if sys.argv[i].startswith('n='):
            try:
                skp = int(sys.argv[i].split('=')[-1])
                qtd = skp
            except ValueError as ex:
                print('O parametro está incorreto')
                print("\tn=[num]\t pula [num] arquivo(s)")
                exit()      
        elif sys.argv[i] == '-l':
            if os.path.exists('log_verifica.txt'):
                try:
                    with open('log_verifica.txt','r') as f_log:
                        skp = int(f_log.readline())
                        qtd = skp
                except IOError as ex:
                    print('Erro:' + ex)
            else:
                print('arquivo log_verifica.txt não existe')
        elif sys.argv[i] == '-h':
            help()
            exit()
        else:
            print('parametro não existe, utilize -h')
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

        print('File:['+str(n)+'] - '+img_file.name)

        fig, ax = plt.subplots(1)        

        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()
        
        key = plt.connect('key_press_event',onkeypress)
        Util.exibe_imagem(img_file,xml_file,ax,fig)
        plt.show()

        qtd += 1
        with open('log_verifica.txt','w') as f_log:
            f_log.write(str(qtd))

        os.system('clear')
        legenda()

