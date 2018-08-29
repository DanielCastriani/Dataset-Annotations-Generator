import sys
import os
import xml.etree.ElementTree as ET
from lxml import etree

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Passe o caminho por argumento")
        exit()
        
    output = sys.argv[1]#'/home/daniel/Desktop/output'

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
        
        for n,image_file in enumerate(os.scandir(image_folder)):
            img = image_file
            xml_path = os.path.join(xml_folder,img.name.replace('png','xml'))
            if os.path.exists(xml_path):
                img_path = img.path

                rename = False
                if ' ' in img_path:
                    img_path = img_path.replace(' ', '\ ')
                    xml_path = xml_path.replace(' ', '\ ')
                    rename = True

                os.system('cp {file} {out_path}'.format(file = img_path,out_path = o_img))
                os.system('cp {file} {out_path}'.format(file = xml_path,out_path = o_xml))

                if '-' in img_path:
                    rename = True

                if rename:
                    ni = os.path.join(output,image_folder,img_path.split('/')[-1]).replace('\ ','')
                    ni = ni.replace('-','_')
                    
                    oi = os.path.join(output,image_folder,img_path.split('/')[-1])
                    os.system('mv {old} {new}'.format(old = oi,new = ni))

                    nx = os.path.join(output,xml_folder,xml_path.split('/')[-1]).replace('\ ','')
                    nx = nx.replace('-','_')

                    ox = os.path.join(output,xml_folder,xml_path.split('/')[-1])
                    os.system('mv {old} {new}'.format(old = ox,new = nx))

                    tree = ET.parse(nx)
                    root = tree.getroot()

                    tree.find('filename').text = ni.split('/')[-1]

                    xml_str = ET.tostring(root)
                    r = etree.fromstring(xml_str)
                    xml_str = etree.tostring(r,pretty_print=True)

                    with open(nx,'wb') as temp_xml:
                        temp_xml.write(xml_str)
                        

                
                print(xml_path)
                print(img_path)
                qtd+=1
                print('------------------------------------------')

        print('Imgs e xml:'+str(qtd))
    else:
        print('path n~ao existe')