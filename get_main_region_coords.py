import pyautogui
import os
import numpy as np
from typing import Tuple, List, Dict
import time
from dotenv import load_dotenv
from pyautogui import ImageNotFoundException
from xiuxian_exception import TargetRegionNotFoundException
from datetime import datetime
import adbutils
# from matplotlib import image

load_dotenv()


# main_region_coords = os.getenv('MAIN_REGION_COORDS')
# main_region_coords = tuple(map(int, main_region_coords.split(',')))
# print(f"获取游戏界面坐标: {main_region_coords}")
# print(f"设备: {device}")

def get_region_coords(
    target_region_image, 
    main_region_coords=None, 
    confidence=0.7,
    grayscale=False,
    root_dir=None,
    cat_dir=None
):
    if cat_dir is not None:
        root_dir = os.path.join(root_dir, cat_dir)
    
    if root_dir is None:
        root_dir = os.getenv('ROOT_DIR')


    image_path = os.path.join(root_dir, f'{target_region_image}.png')
    
    try:
        # 在登录页面区域内定位指定区域的坐标
        if main_region_coords is not None:
            region_coords = pyautogui.locateOnScreen(
                image_path,
                region=main_region_coords,
                confidence=confidence,
                grayscale=grayscale
            )
        else:
            region_coords = pyautogui.locateOnScreen(
                image_path,
                confidence=confidence,
                grayscale=grayscale
            )
    except ImageNotFoundException:
        region_coords = None

    return region_coords

def get_game_page_coords(resolution=(1080, 1920)):
    # 在屏幕上定位登录页面的坐标
    game_page_coords = None
    # for game_page in ['shouye', 'login_page', 'user_custom']:
    for game_page in ['shouye', 'user_custom']:
        if game_page == 'shouye':
            shouye_coords = get_region_coords('shouye', grayscale=True)
            if shouye_coords is None:
                continue

            left_bottom_x = shouye_coords[0]
            left_bottom_y = shouye_coords[1] + shouye_coords[3]
            return (left_bottom_x, left_bottom_y, resolution[0], resolution[1] )
        
        game_page_coords = pyautogui.locateOnScreen(
            './FanRenXiuXianIcon_{}_{}/{}.png'.format(resolution[0], resolution[1], game_page),
            confidence=0.95
        )
        if game_page_coords is not None:
            return game_page_coords
    
    raise Exception('未定位到游戏界面')

if __name__ == '__main__':
    
    adb = adbutils.AdbClient(host="127.0.0.1", port=5037)

    serial = "emulator-5566"
    device = adb.device(serial=serial)


    resolution = (540, 960)
    os.environ['ROOT_DIR'] = f'FanRenXiuXianIcon_{resolution[0]}_{resolution[1]}'

    main_region_coords = get_game_page_coords(resolution)
    main_region_coords = tuple(map(int, main_region_coords))
    print(f"获取游戏界面坐标: {main_region_coords}")
    print(','.join(map(str, main_region_coords)))

