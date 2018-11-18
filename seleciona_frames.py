import os
import cv2
from matplotlib import pyplot as plt
from matplotlib.widgets import RectangleSelector

image_folder = 'video2img/'

mv_folder = 'video2img_sel'
mv_img = os.path.join(mv_folder,'sel')
mv_trash = os.path.join(mv_folder,"trash")

im_path = None

qtd = 0

def legenda():
    print('[F1] - Seleciona e Proximo')
    print('[F2] - Lixo e Proximo')
    print('--------------------------')


def onkeypress(event):
    global qtd
    if event.key == 'f1':
        if im_path is not None:
            os.system("mv {} {}".format(im_path,mv_img))
            qtd += 1
        plt.close()
    elif event.key == 'f2':
        if im_path is not None:
            os.system("mv {} {}".format(im_path,mv_trash))
            qtd += 1
        plt.close()
    elif event.key == 'q':
        plt.close()
        exit()



def line_select_callback(clk,rls):
    global tl
    global br

    tl = (int(clk.xdata), int(clk.ydata))
    br = (int(rls.xdata), int(rls.ydata))

    print('{} x {}'.format(br[0] - tl[0], br[1] - tl[1]))


def toggle_selector(event):
    toggle_selector.RS.set_active(True)


def order_by(elm):
    return elm[1].name


if __name__ == '__main__':
    if not os.path.exists(mv_folder):
        os.mkdir(mv_folder)

    if not os.path.exists(mv_img):
        os.mkdir(mv_img)

    if not os.path.exists(mv_trash):
        os.mkdir(mv_trash)

    all_files = sorted(enumerate(os.scandir(image_folder)), key=order_by)

    lenth = len(all_files)

    for n,image_file in all_files:

        os.system("clear")
        legenda()
        im_path = image_file.path
        print(im_path)
        print('{}/{}'.format(qtd, lenth))

        fig, ax = plt.subplots(1)
        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()

        image = cv2.imread(image_file.path)
        if image is None:
            continue
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        ax.imshow(image)

        toggle_selector.RS = RectangleSelector(
            ax,line_select_callback ,
            drawtype='box',useblit=True,
            button=[1],
            minspanx=5,minspany=5,
            spancoords='pixels',interactive=True
        )
        bbox = plt.connect('key_press_event', toggle_selector)
        key = plt.connect('key_press_event', onkeypress)
        plt.show()