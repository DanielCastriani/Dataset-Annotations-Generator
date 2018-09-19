# pylint: disable=E1101
import sys
import os
import xml.etree.ElementTree as ET
import cv2
from lxml import etree
from EfxUtil import Efx

qtd = 0
output = ''
image_folder = ''
xml_folder = ''


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

def transformacao(xml,image_path):
    img_efx = Efx(image_path)

    #Brilho
    gera_arquivo(xml,img_efx.filter_brightnes_contrast(30,1))
    gera_arquivo(xml,img_efx.filter_brightnes_contrast(20,1))
    gera_arquivo(xml,img_efx.filter_brightnes_contrast(-20,1))
    gera_arquivo(xml,img_efx.filter_brightnes_contrast(-30,1))

    #Contraste
    gera_arquivo(xml,img_efx.filter_brightnes_contrast(0,0.7))
    gera_arquivo(xml,img_efx.filter_brightnes_contrast(0,0.8))
    gera_arquivo(xml,img_efx.filter_brightnes_contrast(0,1.2))
    gera_arquivo(xml,img_efx.filter_brightnes_contrast(0,1.3))


    

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

        for n,image_file in enumerate(os.scandir(image_folder)):
            img = image_file
            xml_path = os.path.join(xml_folder,img.name.replace('png','xml'))
            if os.path.exists(xml_path):
                try:
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

                    xml_str = ET.tostring(root)
                    r = etree.fromstring(xml_str)
                    xml_str = etree.tostring(r,pretty_print=True)

                    with open(nx,'wb') as temp_xml:
                        temp_xml.write(xml_str)  

                    qtd+=1
                    qtd_arq+=1
                    transformacao(tree,ni)
                    print(str(qtd) + "\t"+ str(qtd_arq) +"/" + str(qtd_files))
                    print('------------------------------------------')
                except IOError as err:
                    log += '--------------------------------------\n'+'Error Message:' + err.strerror+'\n'+'files\n' + xml_path + '\n'+ img_path + '\n'+'--------------------------------------'

        print('Imgs e xml:'+str(qtd))
        if len(log) > 0:
            with open('err_log.txt','w') as f:
                f.write(log)
    else:
        print('path n~ao existe')
    