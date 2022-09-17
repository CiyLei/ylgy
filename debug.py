import cv2

DEBUG = True
SHOW_WINDOWS = '测试窗口'


def debug_show(img, info=''):
    if DEBUG:
        if len(info) > 0:
            print(info)
        cv2.imshow(SHOW_WINDOWS, img)
        cv2.waitKey(200)

