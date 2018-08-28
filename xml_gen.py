#pylint: disable=E1101

import os
import matplotlib.pyplot as plt
import cv2
from matplotlib.widgets import RectangleSelector
import xml_writer as w_xml

img = None
tl_list = []
br_list = []
object_list = []
tl = (0,0)
br = (0,0)

qtd_imgs = 0

image_folder = 'images'
savedir = 'annotation'
obj = 'placa'

def line_select_callback(clk,rls):
    global tl
    global br

    tl = (int(clk.xdata),int(clk.ydata))
    br = (int(rls.xdata),int(rls.ydata))

def toggle_selector(event):
    toggle_selector.RS.set_active(True)

def onkeypress(event):
    global object_list
    global tl_list
    global br_list
    global tl
    global br
    global img
    
    if event.key == 'q' or event.key == 'escape':
        w_xml.write_xml(image_folder,img,object_list,tl_list,br_list,savedir)       
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

        print(object_list[-1],'\ttl:',tl,'\tbr:',br)

if __name__ == '__main__':
    
    print('[F1] - Add placa_de_regulamentacao')
    print('[F2] - Add placa_de_advertencia')
    print('[F3] - Add pare')
    print('[F4] - Add de_preferencia')
    print('[F5] - Add marcador_alimnhamento')
    print('[F6] - Add marcador_de_perigo')

    print('\n\n[Q] ou [ESQ] - Proxima Imagem')

    print('*Sempre adicionar da esquerda para a direita, e de baixo para cima')

    for n,image_file in enumerate(os.scandir(image_folder)):
        tl_list = []
        br_list = []
        object_list = []
        tl = (0,0)
        br = (0,0)
        img = image_file

        qtd_imgs += 1

        if not os.path.isdir(savedir):
            os.mkdir(savedir)

        verifica_existe = os.path.join(savedir,img.name.replace('png','xml'))
        if os.path.exists(verifica_existe):
            continue


        print('{}'.format(qtd_imgs))

        fig, ax = plt.subplots(1)        
        
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