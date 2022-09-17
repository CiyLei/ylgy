from time import sleep
import win32.win32gui as win32gui
import pyautogui
import cv2
import numpy as np
from debug import *
from entity import *

def main():

    # 寻找羊了个羊窗口
    handle = win32gui.FindWindow(None, '羊了个羊')
    w_left, w_top, w_right, w_bottom = win32gui.GetWindowRect(handle)
    print('羊了个羊 窗口位置：', w_left, w_top, w_right, w_bottom)
    # 截屏
    w_img = pyautogui.screenshot(region=(w_left, w_top, w_right - w_left, w_bottom - w_top))

    img = cv2.cvtColor(np.asarray(w_img), cv2.COLOR_RGB2BGR)
    original = cv2.copyTo(img, img)
    debug_show(img, '加载图片')
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    debug_show(img, '灰值化')
    cv2.bitwise_not(img, img)
    debug_show(img, '反转颜色')
    # img = cv2.GaussianBlur(img, (3, 3), 5)
    # debug_show(img, '高斯模糊')
    _, img = cv2.threshold(img, 30, 255, cv2.THRESH_BINARY)
    debug_show(img, '二值化')
    # img = cv2.erode(img, np.ones((2, 2)))
    # debug_show(img, '腐蚀膨胀')
    cv2.bitwise_not(img, img)
    debug_show(img, '反转颜色')
    # 寻找轮廓
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    img_height = img.shape[0]
    main_contours = []
    bottom_contours = []
    img = cv2.copyTo(original, original)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        # print(x, y, w, h)
        # img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
        if w > 35 and w < 80 and h > 35 and h < 80:
            color = (0, 0, 255)
            if y > img_height * 0.7:
                bottom_contours.append((x, y, w, h))
                color = (255, 0, 0)
            else:
                main_contours.append((x, y, w, h))
            img = cv2.rectangle(img, (x, y), (x + w, y + h), color, 5)
    debug_show(img, '加载轮廓')

    entity_list = []
    for contour in main_contours:
        entity = Entity(original, contour)
        if entity.type == 0: continue
        entity_list.append(entity)
        cv2.putText(img, str(entity.type), entity.point(offset_y=15), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 2)
    for contour in bottom_contours:
        entity = Entity(original, contour, True)
        if entity.type == 0: continue
        entity_list.append(entity)
        cv2.putText(img, str(entity.type), entity.point(offset_y=15), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0), 2)
    debug_show(img, '加载类型')
    print(f'找到实体:{entity_list}')
    # 游戏结束
    if len(entity_list) == 0:
        pyautogui.click(w_left + 300, w_top + 800)
        sleep(3)
        pyautogui.click(w_left + 300, w_top + 900)
        sleep(3)
        return

    # 根据类型聚合
    entity_map = dict()
    for entity in entity_list:
        if not entity_map.__contains__(entity.type):
            entity_map[entity.type] = [entity]
        else:
            entity_map[entity.type].append(entity)
    # 添加指令
    action_list = []
    for key in entity_map:
        values = entity_map[key]
        values = sorted(values, key=lambda e: 0 if e.is_bottom else 1)
        if len(values) >= 3:
            i = 0
            for entity in values:
                if not entity.is_bottom: 
                    action_list.append(entity)
                i += 1
                if i >= 3:
                    break
    if len(action_list) == 0:
        print("无指令，选最多的")
        main_map = {}
        for key in entity_map:
            values = entity_map[key]
            for entity in values:
                if not entity.is_bottom:
                    if not main_map.__contains__(entity.type):
                        main_map[entity.type] = 1
                    else:
                        main_map[entity.type] += 1
        sort_list = sorted(main_map.items(), key=lambda e: e[1], reverse=True)
        action_list.extend(entity_map[sort_list[0][0]])
        print(f"无指令，选择：{action_list}")
                
    # 执行指令
    for action in action_list:
        print(action)
        x, y, w, h = action.contour
        pyautogui.click(w_left + x + w / 2, w_top + y + h / 2)
        sleep(1)

    cv2.waitKey(1000)
    # cv2.waitKey()

if __name__ == '__main__':
    main()