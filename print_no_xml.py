#pylint: disable=E1101

import os
import sys
import matplotlib.pyplot as plt
import cv2
from matplotlib.widgets import RectangleSelector
import class_counter as c_count
import numpy as np
import Util
import time

exts = ['png','PNG','jpg','JPG']

image_folder = 'images'
savedir = 'annotations'
obj = 'placa'

verbose = False
v_c_count = False
preview = False
reverso = False
skp_nome_f = False
skp_nome = ""

skp = 0
qtd = 0

img = None
n = 0
tl = (0,0)
br = (0,0)

fig = None
ax = None
image = None


def line_select_callback(clk,rls):
    global tl
    global br

    tl = (int(clk.xdata),int(clk.ydata))
    br = (int(rls.xdata),int(rls.ydata))
    if preview:
        pass

def toggle_selector(event):
    toggle_selector.RS.set_active(True)

def cropp():
    global img
    global tl,br
    global img_path
    global image

    h,w = (br[1]+1) - tl[1] ,  (br[0]+1) - tl[0]
    print(w,' x ',h)


    if not os.path.exists('print_output'):
        os.mkdir('print_output')

    image = cv2.imread(img.path)
    image = image[tl[1]:br[1] , tl[0]:br[0]]

    img_path = 'print_output/imagem {}.png'.format(time.time())
    cv2.imwrite(img_path,image)    

def onkeypress(event):
    global object_list
    global tl_list
    global br_list
    global tl
    global br
    global img
    global exts
    global skp
    global skp_nome
    global skp_nome_f
    global image

    if event.key == ' ':      
        tl_list = []
        br_list = []
        img = None
        plt.close()
    elif event.key == 'escape':
        plt.close()
    elif event.key == 'c':
        cropp()
    elif event.key == 'q' or event.key == 'f12' :
        exit()     

def legenda():
    if verbose:
        Util.plt_legenda()
        print('\n[Space] - Proxima Imagem')
        print('\n[C] - Print')
        print('[Enter] - Pula imagens até inicio do nome ser diferente')        
        print('[Q] ou [F12] - Sair')
    
    if verbose and img is not None:
        print('File:['+str(n)+'] - '+img.name)

def order_by(elm):
    return elm[1].name

def help():
    print("Parametros")
    print("\t-p \tPreview\n")
    print("\t-a \tTodas as opções")
    print("\t-r \tOrdenar reverso")
    print("\tn=[num]\t pula [num] arquivo(s)")

if __name__ == '__main__':
    
    if len(sys.argv) == 1:
        help()

    verbose = True
    for i in range(1,len(sys.argv)):
        if sys.argv[i] == '-h':
            help()
            exit()
        elif sys.argv[i] == '-c':
            v_c_count = True
        elif sys.argv[i] == '-r':
                reverso = True
        elif sys.argv[i] == '-a':
            verbose = True
            v_c_count = True
            preview = True
        elif sys.argv[i].startswith('n='):
            try:
                skp = int(sys.argv[i].split('=')[-1])
            except ValueError as ex:
                print('O parametro está incorreto utiliza -h')
                exit()
        elif sys.argv[i] == '-l':
            if os.path.exists('log_print.txt'):
                try:
                    with open('log_print.txt','r') as f_log:
                        skp = int(f_log.readline())
                        qtd = skp
                except IOError as ex:
                    print('Erro:' + ex)
        else:
            print('parametro não existe, utilize -h')
            exit()

    sc_dir = os.scandir(image_folder)
    
    all_files = sorted(enumerate(sc_dir),key=order_by,reverse=reverso)

    for n,image_file in all_files:
        qtd += 1

        if skp_nome_f:
            if skp_nome in image_file.name:
                continue
            else:
                skp_nome_f = False

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
        
        if '_rotate' in image_file.name:
            continue

        tl_list = []
        br_list = []
        object_list = []
        tl = (0,0)
        br = (0,0)
    
        if verbose:
            os.system('clear')
            legenda()    

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

        with open('log_xml_gen.txt','w') as f_log:
            f_log.write(str(qtd))