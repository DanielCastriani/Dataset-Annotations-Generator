import xml.etree.ElementTree as ET
import os

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

#_,_,s = count()
#print(s)