import xml.etree.ElementTree as ET
import os
import sys
import datetime

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
    qtd_gerada = 8

    dt = datetime.datetime(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day).timestamp()
    
    dir = 'annotations'
    cl = []
    qtd = []
    qtd_arqs = 0
    qtd_dia = 0
    for _, f_xml in enumerate(os.scandir(dir)):
        if f_xml.name.endswith('xml') == True:
            qtd_arqs += 1
            tree = ET.parse(f_xml)
            root = tree.getroot()
            find(root,cl,qtd)     

            dt_modificado = os.path.getmtime(f_xml)
            
            if dt_modificado > dt:
                qtd_dia += 1
            
    s = ''
    total_qtd = 0 
    s += 'Classe [real ,real x ' + str(qtd_gerada) + ']' + '\n\n'
    for i in range(len(qtd)):
       s+= cl[i]+'\t['+str(qtd[i])+','+str(qtd[i] * qtd_gerada)+']\n'
       total_qtd += qtd[i]
    s += '\nTotal de objetos:' + str(total_qtd) + ' / ' + str(total_qtd * qtd_gerada)
    s += '\nTotal de arquivos:' + str(qtd_arqs)+ ' / ' + str(qtd_arqs * qtd_gerada)
    s += '\nTotal de arquivos no dia:' + str(qtd_dia)
    return cl,qtd,s

def verifica_xml_img():
    """
    Retorna
        n = numero de arquivos
        log = paths
    """
    exts = ['png','PNG','jpg','JPG']
    log = ''
    n = 0
    ann_dir = 'annotations'     
    img_dir = 'images'  

    salva = False

    for _, f_xml in enumerate(os.scandir(ann_dir)):
        n +=1
        existe = False
        for ext in exts:
            verifica = os.path.join(img_dir,f_xml.name.replace('.xml','.' + ext))
            if os.path.exists(verifica):
                existe = True
                break
        
        if not existe:
            log += f_xml.path + '\n'
            log += '-----------------------------------------------\n'
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