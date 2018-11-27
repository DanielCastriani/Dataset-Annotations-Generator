import cv2
import xml.etree.ElementTree as ET

from Cython.Compiler.ExprNodes import _analyse_name_as_type


def hb1():
    print('_________________________________________________________________')

def hb2():
    print('--------------------------------------------')

def _plt_legenda():
    print('[R] ou [H] ou [Home] - Reset')
    print('[P] - Pan (Mover)')
    print('[O] - Zoom')

def plt_legenda():
    hb2()
    _plt_legenda()
    hb2()

def cores():
    return [tuple([0,255,0]),tuple([0,255,255]),tuple([0,0,255]),tuple([255,0,0]),tuple([255,255,255]),tuple([255,255,0])]

def getCor(label):
    if label == "regulamentacao":
        return cores()[0]
    elif label == "advertencia":
        return cores()[1]
    elif label == "pare":
        return cores()[2]
    elif label == "de_preferencia":
        return cores()[3]
    elif label == "marcador_alimnhamento":
        return cores()[4]
    elif label == "marcador_de_perigo":
        return cores()[5]
    
def exibe_bound_box(image,xml_file,pixel_size = 1):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        lb = obj.find('name').text            
        bb = obj.find('bndbox')
        tl = (int(bb.find('xmin').text), int(bb.find('ymin').text))
        br = int(bb.find('xmax').text), int(bb.find('ymax').text)

        cor = getCor(lb)
        pos_txt = (tl[0],tl[1] - 5)
        image = cv2.rectangle(image, tl, br, cor, 1)
        image = cv2.putText(image, lb, pos_txt, cv2.FONT_HERSHEY_COMPLEX, 0.5, cor, 1)

    return image

def exibe_imagem(img_file,xml_file,ax,fig):
    image = cv2.imread(img_file.path)
    image = exibe_bound_box(image,xml_file)
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    ax.imshow(image)
    fig.canvas.draw()
    fig.canvas.flush_events()

def exibe_imagem_xy(image,labels,tls,brs,ax,fig):
    image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
    for i in range(0,len(labels)):
        cor = getCor(labels[i])   
        image = cv2.rectangle(image, tls[i], brs[i], cor, 2)    
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    ax.imshow(image)
    fig.canvas.draw()
    fig.canvas.flush_events()

def replace_classe(str):
    dict = {
        "regulamentacao": "placa",
        "advertencia": "placa",
        "pare": "placa",
        "de_preferencia": "placa",
        "marcador_alimnhamento": "placa",
        "marcador_de_perigo": "placa"
    }
    return dict[str]

def exts():
    return ['png','PNG','jpg','JPG']

if __name__ == '__main__':
    print(replace_classe('regulamentacao'))
    print(replace_classe('advertencia'))
    print(replace_classe('pare'))
    print(replace_classe('de_preferencia'))
    print(replace_classe('marcador_alimnhamento'))
    print(replace_classe('marcador_de_perigo'))
