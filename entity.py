import cv2
from skimage.metrics import structural_similarity
from skimage.metrics import peak_signal_noise_ratio
import numpy as np


class Entity(object):

    TYPE_1 = cv2.imread('img\i1.png')
    TYPE_2 = cv2.imread('img\i2.png')
    TYPE_3 = cv2.imread('img\i3.png')
    TYPE_4 = cv2.imread('img\i4.png')
    TYPE_5 = cv2.imread('img\i5.png')
    TYPE_6 = cv2.imread('img\i6.png')
    TYPE_7 = cv2.imread('img\i7.png')
    TYPE_8 = cv2.imread('img\i8.png')
    TYPE_9 = cv2.imread('img\i9.png')
    TYPE_10 = cv2.imread('img\i10.png')
    TYPE_11 = cv2.imread('img\i11.png')
    TYPE_12 = cv2.imread('img\i12.png')
    TYPE_13 = cv2.imread('img\i13.png')
    TYPE_14 = cv2.imread('img\i14.png')
    TYPE_15 = cv2.imread('img\i15.png')

    TYPE_LIST = [TYPE_1, TYPE_2, TYPE_3, TYPE_4, TYPE_5, TYPE_6, TYPE_7,
                 TYPE_8, TYPE_9, TYPE_10, TYPE_11, TYPE_12, TYPE_13, TYPE_14, TYPE_15]

    def __init__(self, img, contour, is_bottom=False):
        x, y, w, h = contour
        self.contour = contour
        self.img = img[y:y+h, x:x+w]
        self.type = 0
        self.is_bottom = is_bottom
        max_compare = 0
        for i in range(len(Entity.TYPE_LIST)):
            img_type = Entity.TYPE_LIST[i]
            compare_value = _compare(img_type, self.img)
            if compare_value > 0.5 and compare_value > max_compare:
                max_compare = compare_value
                self.type = i + 1
        self.compare_value = max_compare

    def __str__(self) -> str:
        return f'type: {self.type},point:{self.contour},is_bottom:{self.is_bottom},compare_value:{self.compare_value}'

    def __repr__(self) -> str:
        return f'type: {self.type},point:{self.contour},is_bottom:{self.is_bottom},compare_value:{self.compare_value}'

    def point(self, offset_x=0, offset_y=0):
        x, y, _, _ = self.contour
        return (x + offset_x, y + offset_y)


def _compare(img1, img2):
    img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2RGBA)
    img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2RGBA)
    img1 = cv2.resize(img1, (15, 15))
    img2 = cv2.resize(img2, (15, 15))
    # img1 = img1[0:min(img1.shape[0],img2.shape[0]),0:min(img1.shape[1],img2.shape[1]),0:4]
    # img2 = img2[0:min(img1.shape[0],img2.shape[0]),0:min(img1.shape[1],img2.shape[1]),0:4]

    # img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
    # img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
    # img1 = img1[0:min(img1.shape[0],img2.shape[0]),0:min(img1.shape[1],img2.shape[1])]
    # img2 = img2[0:min(img1.shape[0],img2.shape[0]),0:min(img1.shape[1],img2.shape[1])]

    score = structural_similarity(
        img1, img2, multichannel=True, channel_axis=4)

    # score = peak_signal_noise_ratio(img1, img2)
    return score

# if __name__ == '__main__':
#     img1 = cv2.imread('img\error.png')
#     # img2 = cv2.imread('img\i4.png')
#     img1 = cv2.resize(img1, (60, 60))
#     # img2 = cv2.resize(img2, (60, 60))
#     img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
#     # img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
#     # score, diff = structural_similarity(img1, img2, full=True)
#     # print(score)
#     for i in range(len(Entity.TYPE_LIST)):
#         img2 = Entity.TYPE_LIST[i]
#         img2 = cv2.resize(img2, (60, 60))
#         # img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
#         img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
#         score, diff = structural_similarity(img1, img2, full=True)
#         print(score)
