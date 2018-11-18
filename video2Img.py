import cv2
import time,os

def order_by(elm):
    return elm[1].name

ini = time.time()

video_path_folder = './videos'

if os.path.exists(video_path_folder):

    if not os.path.exists('video2img'):
        os.mkdir('video2img')

    img_path = 'video2img/img_{}.jpg'
    num = 1

    all_files = sorted(enumerate(os.scandir(video_path_folder)), key=order_by, reverse=False)

    for _,file in all_files:
        video_path = file.path
        capture = cv2.VideoCapture(video_path)

        print(video_path)

        count = 0
        length = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        ret, frame = capture.read()

        while count <= length:
            if count % 4 == 0:
                cv2.imwrite(img_path.format(num),frame)
                num += 1
                print("{} / {}".format(count,length))
            count += 1
            ret, frame = capture.read()

else:
    print('Path não encontrado')

print(time.time() - ini)