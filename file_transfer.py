import os
from shutil import copy2

img_folder = 'images'
ann_folder = 'annotations'
n_folder = 'output_files'

img_n_folder = os.path.join(n_folder,img_folder)
ann_n_folder = os.path.join(n_folder,ann_folder)


total_xml_files = len(os.listdir(ann_folder))

if not os.path.exists(n_folder):
    os.mkdir(n_folder)
    os.mkdir(img_n_folder)
    os.mkdir(ann_n_folder)
else:
    print('{}/ existe, processo abortado!!!'.format(n_folder))
    exit()


x = 0
p = round(total_xml_files / 100)

for n,image_file in enumerate(os.scandir(img_folder)):
    img_name = image_file.name
    xml_name = image_file.name.split('.')[0] + '.xml'

    xml_path = os.path.join(ann_folder,xml_name)

    if os.path.exists(xml_path):
        x += 1
        if x % p == 0:
            print('{}/{} {}%\n'.format(x,total_xml_files, (x*100/total_xml_files)))
        
        n_xml_file = os.path.join(n_folder,xml_path)
        n_img_path = os.path.join(n_folder,image_file.path)

        copy2(image_file.path,n_img_path)
        copy2(xml_path,n_xml_file)

        err = False
        if not os.path.exists(n_xml_file):
            print('Erro ao copiar {}'.format(n_xml_file))
            err = True
        if not os.path.exists(n_img_path):
            print('Erro ao copiar {}'.format(n_img_path))
            err = True

        if err:
            x -= 1
print('{}/{} {}%\n'.format(x,total_xml_files, (x*100/total_xml_files)))
print('Fim')
            