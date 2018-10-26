import xml.etree.ElementTree as ET
import os
import sys
import datetime

folder = '.'

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
    return classes,QTD,qtd_arqs_xml,Str
    """
    qtd_gerada = 4

    dt = datetime.datetime(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day).timestamp()
    
    dir = os.path.join(folder,'annotations')
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
    return cl,qtd,qtd_arqs,s

def verifica_xml_img():
    """
    Retorna
        n = numero de arquivos
        log = paths
    """
    exts = ['png','PNG','jpg','JPG']
    log = ''
    n = 0
    ann_dir = os.path.join(folder,'annotations')
    img_dir = os.path.join(folder,'images')

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
        else:
            tree = ET.parse(f_xml)
            root = tree.getroot()
            objs = root.findall('object')
            for obj in objs:
                bndbx = obj.find('bndbox')
                try:
                    xmin = int(bndbx.find('xmin').text)
                    xmax = int(bndbx.find('xmax').text)
                    ymin = int(bndbx.find('ymin').text)
                    ymax = int(bndbx.find('ymax').text)
                    if xmin > xmax:
                        salva = True                    
                        log += f_xml.path + '\n'
                        log += 'xmin > xmax\n'
                        log += '-----------------------------------------------\n'    
                    if ymin > ymax:
                        salva = True                    
                        log += f_xml.path + '\n'
                        log += 'ymin > ymax\n'
                        log += '-----------------------------------------------\n'                        

                except:
                    salva = True                    
                    log += f_xml.path + '\n'
                    log += 'parse int\n'
                    log += '-----------------------------------------------\n'    
    
    if salva:
        with open('log','w') as log_file:
            log_file.write(log)

    return n,log

if __name__ == '__main__':
    s = ''
    print(sys.argv)
    if len(sys.argv) == 1:
        print('1 - Contar Classes')
        print('2 - Verifica xml x imagem')
    elif len(sys.argv) >= 2:
        if sys.argv[1] == '1':
            if len(sys.argv) == 3:
                folder = sys.argv[2]
                if not os.path.exists(folder):
                    print('Path não existe')
                    exit()
            _,_,_,s = count()
        elif sys.argv[1] == '2':
            n,s = verifica_xml_img()
            print('{} arquivos verificados'.format(n))
    print(s)