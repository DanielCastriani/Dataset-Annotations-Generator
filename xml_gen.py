#pylint: disable=E1101

import os
import sys
import matplotlib.pyplot as plt
import cv2
from matplotlib.widgets import RectangleSelector
import xml_writer as w_xml
import class_counter as c_count
import numpy as np

exts = ['png','PNG','jpg','JPG']

image_folder = 'images'
savedir = 'annotations'
obj = 'placa'

verbose = False
v_c_count = False
preview = False
reverso = False

skp = 0

img = None
tl_list = []
br_list = []
object_list = []
tl = (0,0)
br = (0,0)

def line_select_callback(clk,rls):
    global tl
    global br

    tl = (int(clk.xdata),int(clk.ydata))
    br = (int(rls.xdata),int(rls.ydata))
    if preview:
        pass

def toggle_selector(event):
    toggle_selector.RS.set_active(True)

def onkeypress(event):
    global object_list
    global tl_list
    global br_list
    global tl
    global br
    global img
    global exts
    global skp

    if event.key == 'q' or event.key == 'escape':
        w_xml.write_xml(image_folder,img,object_list,tl_list,br_list,savedir,exts,verbose)       
        tl_list = []
        br_list = []
        img = None
        plt.close()
    elif event.key == ' ':
        skp = 9    
        tl_list = []
        br_list = []
        img = None
        plt.close()
    else:
        add = True
        if event.key == 'f1':
            object_list.append('regulamentacao')
        elif event.key == 'f2':
            object_list.append('advertencia')
        elif event.key == 'f3':
            object_list.append('pare')
        elif event.key == 'f4':
            object_list.append('de_preferencia')
        elif event.key == 'f5':
            object_list.append('marcador_alimnhamento')
        elif event.key == 'f6':
            object_list.append('marcador_de_perigo')
        elif event.key == 'f12':
            exit()
        else:
            add = False
            
        if add == True:
            tl_list.append(tl)
            br_list.append(br)

        if verbose and add:
            print(object_list[-1],'\ttl:',tl,'\tbr:',br,'{} x {}'.format(br[0]-tl[0],br[1]-tl[1]))



def legenda():
    if verbose:
        print('[F1] - Add placa_de_regulamentacao')
        print('[F2] - Add placa_de_advertencia')
        print('[F3] - Add pare')
        print('[F4] - Add de_preferencia')
        print('[F5] - Add marcador_alimnhamento')
        print('[F6] - Add marcador_de_perigo')

        print('\n[Q] ou [ESQ] - Proxima Imagem')
        print('[space] - Pula 9 imagens')
        print('[F12] - Sair')
        print('*Sempre adicionar da esquerda para a direita, e de baixo para cima\n')
        
    if v_c_count:
        _,_,msg = c_count.count()
        print('_________________________________________________________________')
        print(msg)
        print('_________________________________________________________________')
        print(skp)

def order_by(elm):
    return elm[1].name
def help():
    print("Parametros")
    print("\t-v \tSaída")
    print("\t-c \tContador de classes")
    print("\t-p \tPreview\n")
    print("\t-a \tTodas as opções")
    print("\t-r \tOrdenar reverso")
    print("\t-n=[num]\t pula [num] arquivo(s)")

if __name__ == '__main__':
    
    if len(sys.argv) == 1:
        help()

    for i in range(0,len(sys.argv)):
        if sys.argv[i] == '-h':
            help()
            exit()
        if sys.argv[i] == '-v':
            verbose = True
        elif sys.argv[i] == '-c':
            v_c_count = True
        elif sys.argv[i] == '-p':
            preview = True
        elif sys.argv[i] == '-r':
                reverso = True
        elif sys.argv[i] == '-a':
            verbose = True
            v_c_count = True
            preview = True
        elif sys.argv[i].startswith('-n='):
            try:
                skp = int(sys.argv[i].split('=')[-1])
            except ValueError as ex:
                print('O parametro está incorreto utiliza -h')
                exit()

    
    legenda()

    sc_dir = os.scandir(image_folder)
    
    all_files = sorted(enumerate(sc_dir),key=order_by,reverse=reverso)

    for n,image_file in all_files:
        
        if skp > 0:
            skp -= 1
            continue

        img = image_file
        verifica_existe = False

        for ext in exts:            
            if os.path.exists(os.path.join(savedir,img.name.replace(ext,'xml'))):
                verifica_existe = True
                break

        if verifica_existe:
            continue

        tl_list = []
        br_list = []
        object_list = []
        tl = (0,0)
        br = (0,0)

        if verbose:
            print('File:['+str(n)+'] - '+img.name)

        if not os.path.isdir(savedir):
            os.mkdir(savedir)

        fig, ax = plt.subplots(1)        

        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()
        
        image = cv2.imread(image_file.path)
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)

        ax.imshow(image)

        toggle_selector.RS = RectangleSelector(
            ax,line_select_callback ,
            drawtype='box',useblit=True,
            button=[1], #left mouse click
            minspanx=5,minspany=5,
            spancoords='pixels',interactive=True
        )
        bbox = plt.connect('key_press_event',toggle_selector)
        key = plt.connect('key_press_event',onkeypress)
        plt.show()
        if verbose:
            os.system('clear')
            legenda()