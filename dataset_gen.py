import sys
import os
import xml.etree.ElementTree as ET
import cv2
from lxml import etree
from EfxUtil import Efx
import time
import Util

qtd = 0
output = ''
image_folder = ''
xml_folder = ''

replace_classe = False
skip_class = ['marcador_alimnhamento','marcador_de_perigo','de_preferencia']
exts = Util.exts()

def gera_arquivo(xml_tree,img):
    global qtd
    ni = os.path.join(output,image_folder,str(qtd)+'.png')   
    nx = os.path.join(output,xml_folder,str(qtd)+'.xml')
    while os.path.exists(ni):
        qtd += 1
        ni = os.path.join(output,image_folder,str(qtd)+'.png')   

    xml_tree.find('filename').text = ni.split('/')[-1]
    root = tree.getroot()

    xml_str = ET.tostring(root)
    r = etree.fromstring(xml_str)
    xml_str = etree.tostring(r,pretty_print=True)    

    with open(nx,'wb') as temp_xml:
        temp_xml.write(xml_str)  

    cv2.imwrite(ni,img)

    qtd += 1
# alterar prv para a quantidade de transformaçes
prv = 4
def transformacao(xml,image_path):
    img_efx = Efx(image_path)

    #Brilho
    #gera_arquivo(xml,img_efx.filter_brightnes_contrast(30,1))
    gera_arquivo(xml,img_efx.filter_brightnes_contrast(20,1))
    gera_arquivo(xml,img_efx.filter_brightnes_contrast(-20,1))
    #gera_arquivo(xml,img_efx.filter_brightnes_contrast(-30,1))

    #Contraste
    #gera_arquivo(xml,img_efx.filter_brightnes_contrast(0,0.7))
    gera_arquivo(xml,img_efx.filter_brightnes_contrast(0,0.8))
    gera_arquivo(xml,img_efx.filter_brightnes_contrast(0,1.2))
    #gera_arquivo(xml,img_efx.filter_brightnes_contrast(0,1.3))


def order_by(elm):
    return elm[1].name

if __name__ == '__main__':
    
    if len(sys.argv) == 1:
        print("Passe o caminho por argumento, ex:")
        print('python file_transfer.py /home/daniel/Desktop/output')
        exit()

    log = ''

    qtd = 0
    qtd_arq = 0
    image_folder = 'images'
    xml_folder = 'annotations'
    output = sys.argv[1]#'/home/daniel/Desktop/output'

    if not os.path.exists(output):
        print('Path não existe')
        exit()

    image_folder = 'images'
    xml_folder = 'annotations'


    qtd = 0
    qtd_skip = 0

    if os.path.exists(output): 
        o_img = os.path.join(output,image_folder)
        o_xml = os.path.join(output,xml_folder)

        if os.path.exists(o_img) == False:
            os.mkdir(o_img)

        if os.path.exists(o_xml) == False:
            os.mkdir(o_xml)
        
        qtd_files = 0

        for _,_ in enumerate(os.scandir(xml_folder)):
            qtd_files += 1

        t_ini = time.time() * 1000

        for n,image_file in sorted(enumerate(os.scandir(image_folder)),key=order_by):
            img = image_file

            existe = False
            for i in range(len(exts)):
                xml_path = os.path.join(xml_folder, img.name.replace(exts[i], 'xml'))
                if os.path.exists(xml_path):
                    existe = True
                    break

            if existe:
                try:
                    o_tree = ET.parse(xml_path)

                    skip = False
                    for obj in o_tree.findall('object'):
                        for s in skip_class:
                            if obj.find('name').text == s:
                                skip = True
                                break
                        if skip:
                            break

                    if skip:
                        qtd_skip += 1
                        continue

                    img_path = img.path

                    if ' ' in img_path:
                        img_path = img_path.replace(' ', '\ ')
                        xml_path = xml_path.replace(' ', '\ ')
                        rename = True

                    os.system('cp {file} {out_path}'.format(file = img_path,out_path = o_img))
                    os.system('cp {file} {out_path}'.format(file = xml_path,out_path = o_xml))
                                        
                    ni = os.path.join(output,image_folder,str(qtd)+'.png')                
                    oi = os.path.join(output,image_folder,img_path.split('/')[-1])
                    os.system('mv {old} {new}'.format(old = oi,new = ni))

                    nx = os.path.join(output,xml_folder,str(qtd)+'.xml')
                    ox = os.path.join(output,xml_folder,xml_path.split('/')[-1])
                    os.system('mv {old} {new}'.format(old = ox,new = nx))

                    if not os.path.exists(nx):
                        log += '--------------------------------------\n'+'Error Message:N~ao Salvou\n'+'files\n' + xml_path + '\n'+ img_path + '\n'+'--------------------------------------'
                    tree = ET.parse(nx)
                    root = tree.getroot()

                    tree.find('filename').text = ni.split('/')[-1]
                    if replace_classe:
                        for ob in tree.findall('object'):
                            obj_name = ob.find('name')
                            c = obj_name.text
                            n_obj_name = Util.replace_classe(c)
                            obj_name.text = n_obj_name

                    xml_str = ET.tostring(root)
                    r = etree.fromstring(xml_str)
                    xml_str = etree.tostring(r,pretty_print=True)

                    with open(nx,'wb') as temp_xml:
                        temp_xml.write(xml_str)  

                    qtd+=1
                    qtd_arq+=1
                    transformacao(tree,ni)
                    if qtd % 30 == 0 :
                        print(str(qtd) + "\t"+ str(qtd_arq) +"/" + str(qtd_files) + "\t\t\tpreview(qtd*" + str(prv)+ "):" + str(qtd_files + qtd_files*prv))

                        ms = time.time() * 1000 - t_ini
                        print(str(ms/1000) + " s")
                        print('------------------------------------------')
                except IOError as err:
                    log += '--------------------------------------\n'+'Error Message:' + err.strerror+'\n'+'files\n' + xml_path + '\n'+ img_path + '\n'+'--------------------------------------'
            else:
                print("{} n~ao existe".format(xml_path))
                log += "{} n~ao existe".format(xml_path)

        print('Imgs e xml{}:'.format(qtd))
        print('pulou {} imagens'.format(qtd_skip))
        if len(log) > 0:
            with open('err_log.txt','w') as f:
                f.write(log)
    else:
        print('path n~ao existe')
    