import os
import cv2
import xml.etree.cElementTree as ET

output_dir = 'rcnn_to_cnn_images'
img_dir = 'images'
ann_dir = 'annotations'
exc_ann_dir = 'exception_annotations'

xtl = (12,12)
xrb = (12,12)

i = 0


def extract(xml_path,img_file):
    global i

    img = cv2.imread(img_file)
    tree = ET.parse(xml_path)
    root = tree.getroot()

    h,w,_ = img.shape

    size = root.find('size')
    size.find('width').text = str(w)
    size.find('height').text = str(h)
    
    for obj in root.iter('object'):
        bb = obj.find('bndbox')

        class_folder = obj.find('name').text
        out_dir = os.path.join(output_dir,class_folder)
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

        tl = (int(bb.find('xmin').text), int(bb.find('ymin').text))
        br = (int(bb.find('xmax').text), int(bb.find('ymax').text))

        xmin = tl[0] - xtl[0] if tl[0] - xtl[0] > 0 else 0
        ymin = tl[1] - xtl[1] if tl[1] - xtl[1] > 0 else 0
        tl  = (xmin,ymin)

        xmax = br[0] + xrb[0] if br[0] + xrb[0] < w else w
        ymax = br[1] + xrb[1] if br[1] + xrb[1] < h else h
        br  = (xmax,ymax)

        path = os.path.join(out_dir,'image_{}.png'.format(i))
        i += 1

        n_image = img[tl[1]:br[1] , tl[0]:br[0]]
        cv2.imwrite(path,n_image)


def order_by(elm):
    return elm[1].name


if not os.path.exists(output_dir):
    os.mkdir(output_dir)

all_files = os.scandir(img_dir)

total = len(os.listdir(ann_dir))
p = round(total/100)

f = 0
f2 = 0


for _,img_file in sorted(enumerate(all_files),key=order_by):
    
    img_name = img_file.name
    xml_name = img_file.name.split('.')[0] + '.xml'
    
    xml_path = os.path.join(ann_dir,xml_name)

    if not os.path.exists(xml_path):    
        continue

    f += 1

    if '_rotate' in xml_path:
        continue

    if os.path.exists(exc_ann_dir):
        verifica_exc = os.path.join(exc_ann_dir,xml_name)
        if os.path.exists(verifica_exc):
            continue
        
    extract(xml_path,img_file.path)
    f2 += 1
    if f % p == 0:
        print('{}/{} - {} \t{} %'.format(f,total,f2, round(f*100/total)))

print('{}/{}\t{} %'.format(f,total, round(f*100/total)))