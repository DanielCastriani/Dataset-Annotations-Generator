#pylint: disable=E1101

import os
import sys
import matplotlib.pyplot as plt
import cv2
from matplotlib.widgets import RectangleSelector

from Utils import xml_writer as w_xml
from Utils import class_counter as c_count
from Utils import Util

exts = ['png','PNG','jpg','JPG']

image_folder = 'images'
savedir = 'annotations'
obj = 'placa'

verbose = False
v_c_count = False
preview = False
reverso = False
skp_nome_f = False
skp_rotated = False
skp_nome = ""

skp = 0
qtd = 0

img = None
n = 0
tl_list = []
br_list = []
object_list = []
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

    if event.key == 'escape':
        w_xml.write_xml(image_folder,img,object_list,tl_list,br_list,savedir,exts,verbose)       
        tl_list = []
        br_list = []
        img = None
        plt.close()
    elif event.key == 'enter':
        skp = 15    
        tl_list = []
        br_list = []
        img = None
        plt.close()
    elif event.key == ' ':
        skp_nome = img.name.split('_rotate')[0]
        skp_nome_f = True
        plt.close()
    elif event.key == '=':
        tl_list = []
        br_list = []
        object_list = []    
        Util.exibe_imagem_xy(image,object_list,tl_list,br_list,ax,fig)
        if verbose:
            os.system('clear')
            legenda()      
    elif event.key == '-' and len(object_list) > 0:
        tl_list.pop()
        br_list.pop()
        object_list.pop()    
        Util.exibe_imagem_xy(image,object_list,tl_list,br_list,ax,fig)
        if verbose:
            os.system('clear')
            legenda()       
            for i in range(0,len(object_list)):
                print(object_list[i],'\ttl:',tl_list[i],'\tbr:',br_list[i],'{} x {}'.format(br_list[i][0] - tl_list[i][0],br_list[i][1] - tl_list[i][1]))
    elif event.key == 'q' or event.key == 'f12' :
        exit()          
    
    elif tl != (0,0) or br != (0,0):
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
        else:
            add = False
            
        if add == True:
            tl_list.append(tl)
            br_list.append(br)
            Util.exibe_imagem_xy(image,object_list,tl_list,br_list,ax,fig)

            if verbose and add:
                os.system('clear')
                legenda()       
                for i in range(0,len(object_list)):
                    print(object_list[i],'\ttl:',tl_list[i],'\tbr:',br_list[i],'{} x {}'.format(br_list[i][0] - tl_list[i][0],br_list[i][1] - tl_list[i][1]))

            tl = (0,0)
            br = (0,0)
            



def legenda():
    if verbose:
        print('[F1] - Add placa_de_regulamentacao')
        print('[F2] - Add placa_de_advertencia')
        print('[F3] - Add pare')
        print('[F4] - Add de_preferencia')
        print('[F5] - Add marcador_alimnhamento')
        print('[F6] - Add marcador_de_perigo')

        Util.plt_legenda()
        print('\n[ESQ] - Proxima Imagem')
        print('[Enter] - Pula 9 imagens')
        print('[Space] - Pula imagens até inicio do nome ser diferente')
        print('[=] - Limpa lista')
        print('[-] - Remove ultimo')
        print('[Q] ou [F12] - Sair')
        print('*Sempre adicionar da esquerda para a direita, e de baixo para cima')
        
    if v_c_count:
        _,_,_,msg = c_count.count()
        print('_________________________________________________________________')
        print(msg)
        print('_________________________________________________________________')
        print('N: ' + str(qtd))
    
    if verbose and img is not None:
        print('File:['+str(n)+'] - '+img.name)

def order_by(elm):
    return elm[1].name
def help():
    print("Parametros")
    print("\t-v \tSaída")
    print("\t-c \tContador de classes")
    print("\t-p \tPreview\n")
    print("\t-a \tTodas as opções")
    print("\t-r \tOrdenar reverso")
    print("\t-sr \tPula _rotate")
    print("\tn=[num]\t pula [num] arquivo(s)")

if __name__ == '__main__':
    
    if len(sys.argv) == 1:
        help()

    for i in range(1,len(sys.argv)):
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
        elif sys.argv[i] == '-sr':
            skp_rotated = True
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
            if os.path.exists('log_xml_gen.txt'):
                try:
                    with open('log_xml_gen.txt','r') as f_log:
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

        if skp_rotated:
            if '_rotate' in img.name:
                continue

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
            os.system('clear')
            legenda()    

        if not os.path.isdir(savedir):
            os.mkdir(savedir)

        fig, ax = plt.subplots(1) 

        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()
        
        image = cv2.imread(image_file.path)
        if image is None:
            continue
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