import cv2
import time,os

video_path = "./RUA02.MP4"

ini = time.time()

if os.path.exists(video_path):
    print('Arquivo não encontrado')

    if not os.path.exists('video2img'):
        os.mkdir('video2img')

    img_path = 'video2img/img_{}.jpg'
    num = 1

    capture = cv2.VideoCapture(video_path)

    ret, frame = capture.read()

    while True:
        if ret:
            cv2.imwrite(img_path.format(num),frame)
            num += 1
        ret, frame = capture.read()

else:
    print('Arquivo não encontrado')

print(time.time() - ini)