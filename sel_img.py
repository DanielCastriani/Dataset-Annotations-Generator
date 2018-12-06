import os
import numpy as np
import cv2
import shutil

qtd = 50

image_folder = 'images/'
ann_folder = 'annotations/'
out_folder = 'sel_img/'

if not os.path.exists(out_folder):
    os.mkdir(out_folder)

dir_entry = enumerate(os.scandir(image_folder))

list = np.array(list(dir_entry))
for i in range(50):
    random_index = np.arange(list.shape[0])
    np.random.shuffle(random_index)
    list = list[random_index]

count = 0


for l in list:
    img_path = l[1].path

    if 'rotate' in img_path:
        continue

    img_name = l[1].name[:len(l[1].name)-4] + ".xml"
    xml = os.path.join(ann_folder,img_name)

    if os.path.exists(xml):
        continue

    img = cv2.imread(img_path)
    if img is None:
        continue

    shutil.copy2(img_path,out_folder)

    count += 1

    if count >= qtd:
        break

