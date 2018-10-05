#pylint:disable=E1101
import os
import cv2
import numpy as np

wspace = 'cropp_workspace'
img_folder = os.path.join(wspace,'images')
ann_folder = os.path.join(wspace,'annotations')

n_folder = os.path.join( wspace,'output')
img_n_folder = os.path.join(n_folder,'images')
ann_n_folder = os.path.join(n_folder,'annotations')

def order_by(elm):
    return elm[1].name

def getXY(img,side):
    xf = 0
    yf = 0
    if side is 'tl':
        ry = range(0,img.shape[0]) 
        rx = range(0,img.shape[1])
    elif side is 'tr':
        ry = range(0,img.shape[0]) 
        rx = reversed(range(0,img.shape[1]))
        xf = img.shape[1] - 1
    elif  side is 'bl':
        ry = reversed(range(0,img.shape[0]))   
        rx = range(0,img.shape[1])
        yf = img.shape[0] - 1   
    elif  side is 'br':
        ry = reversed(range(0,img.shape[0])) 
        rx = reversed(range(0,img.shape[1]))
        yf = img.shape[0] - 1   
        xf = img.shape[1] - 1       
    else:
        return None

    cy = 0
    cx = 0

    for y in ry:
        px = img[y,xf]
        if px[0] != 0 or px[1] != 0 or px[2] != 0:
            cy = y
            break    
    for x in rx:
        px = img[yf,x]
        if px[0] != 0 or px[1] != 0 or px[2] != 0:
            cx = x
            break
    return (cx,cy)

def getCoords(img):
    """
    return [tl,tr,bl,br]
    
    rl,bl,... = (x,y)
    """
    tl = getXY(img,'tl')
    tr = getXY(img,'tr')
    bl = getXY(img,'bl')
    br = getXY(img,'br')   

    return [tl,tr,bl,br]

def getBndbox(img):
    c = getCoords(img)
    tl = c[0]
    tr = c[1]
    bl = c[2]
    br = c[3]

    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0

    # hr
    if tl[0] < tl[1]:
        x1 = tl[0]
        y1 = tr[1]

        x2 = br[0]
        y2 = bl[1]
    else:
        x1 = bl[0] 
        y1 = tl[1]

        x2 = tr[0]
        y2 = br[1]

    return (x1,y1),(x2,y2)

def run():
    for _,image_file in sorted(enumerate(os.scandir(img_folder)),key=order_by):
        img_name = image_file.name
        xml_name = image_file.name.split('.')[0] + '.xml'

        xml_path = os.path.join(ann_folder,xml_name)

        if 'rotate' in img_name:
            if os.path.exists(xml_path):
                print(img_name)

                img = cv2.imread(image_file.path)
                tl,br = getBndbox(img) 
                

                img = img[tl[1]:br[1] , tl[0]:br[0]]


                im_path = os.path.join(img_n_folder,image_file.name)
                cv2.imwrite(im_path,img)
            
        
if __name__ == '__main__':

    if not os.path.exists(n_folder):
        os.mkdir(n_folder)
        os.mkdir(img_n_folder)
        os.mkdir(ann_n_folder)
    else:
        print('{}/ existe, processo abortado!!!'.format(n_folder))
        #exit()

    run()