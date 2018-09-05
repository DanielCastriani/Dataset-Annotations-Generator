import xml.etree.ElementTree as ET
import os
import sys

def find(p,cl,qtd):

    for obj in p.iter('object'):
        for name in obj.iter('name'):
            if name.text in cl:
                index = cl.index(name.text)
                qtd[index] += 1
            else:
                cl.append(name.text)
                qtd.append(1)



def count():
    """
    return classes,QTD,Str
    """
    dir = 'annotations'
    cl = []
    qtd = []
    qtd_arqs = 0
    for _, f_xml in enumerate(os.scandir(dir)):
        if f_xml.name.endswith('xml') == True:
            qtd_arqs += 1
            tree = ET.parse(f_xml)
            root = tree.getroot()
            find(root,cl,qtd)       
    s = ''
    total_qtd = 0 
    for i in range(len(qtd)):
       s+= cl[i]+':'+str(qtd[i])+'\n'
       total_qtd += qtd[i]
    s += '\nTotal de objetos:' + str(total_qtd)
    s += '\nTotal de arquivos:' + str(qtd_arqs)
    return cl,qtd,s

def verifica_xml_img():
    """
        n = numero de arquivos
        log = paths
    """
    log = ''
    n = 0
    ann_dir = 'annotations'     
    img_dir = 'images'  

    salva = False

    for _, f_xml in enumerate(os.scandir(ann_dir)):
        n +=1
        verifica = os.path.join(img_dir,f_xml.name.replace('.xml','.png'))
        if not os.path.exists(verifica):
            log += f_xml.path + '\n'
            log += verifica + '\n'
            log += '-----------------------------------------------'
            salva = True
    if salva:
        with open('log','w') as log_file:
            log_file.write(log)

    return n,log

if __name__ == '__main__':
    s = ''
    
    
    if len(sys.argv) == 1:
        print('1 - Contar Classes')
        print('2 - Verifica xml x imagem')
    elif len(sys.argv) == 2:
        if sys.argv[1] == '1':
            _,_,s = count()
        elif sys.argv[1] == '2':
            n,s = verifica_xml_img()
            print('{} arquivos verificados'.format(n))
    
    print(s)