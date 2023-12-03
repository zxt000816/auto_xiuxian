import pyautogui
import os
import pytesseract
import re
import cv2
import numpy as np
from typing import Tuple
import time
from dotenv import load_dotenv

load_dotenv()

def get_game_page_coords(resolution=(1080, 1920)):
    # 在屏幕上定位登录页面的坐标
    game_page_coords = None
    for game_page in ['shouye', 'login_page', 'xiulian']:
    # for game_page in ['login_page', 'xiulian']:
        if game_page == 'shouye':
            shouye_coords = get_region_coords('shouye', grayscale=True)
            left_bottom_x = shouye_coords[0]
            left_bottom_y = shouye_coords[1] + shouye_coords[3]
            return (left_bottom_x, left_bottom_y, resolution[0], resolution[1] )
        
        game_page_coords = pyautogui.locateOnScreen(
            './FanRenXiuXianIcon/{}.png'.format(game_page),
            confidence=0.8
        )
        if game_page_coords is not None:
            return game_page_coords
    
    raise Exception('未定位到游戏界面')

def get_region_coords(
    target_region_image, 
    main_region_coords=None, 
    confidence=0.7,
    grayscale=False,
    root_dir=os.getenv('ROOT_DIR'),
    cat_dir=None
):
    if cat_dir is not None:
        root_dir = os.path.join(root_dir, cat_dir)

    image_path = os.path.join(root_dir, f'{target_region_image}.png')

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

    return region_coords

def click_region(region_coords, button='left', seconds=2):
    x, y = pyautogui.center(region_coords)
    pyautogui.click(x, y, button=button)
    time.sleep(seconds)

def click_region_by_x_y(x, y, button='left'):
    pyautogui.click(x, y, button=button)

def move_to_specific_coords(coords: Tuple[int, int], seconds: int = 1):
    x, y = coords
    pyautogui.moveTo(x, y)
    time.sleep(seconds)

def scroll_specific_length(length: int, seconds: int = 5):
    # minus length means scroll down
    # plus length means scroll up
    pyautogui.scroll(length)
    time.sleep(seconds)

def display_region(region_coords):
    # 使用screenShot()方法截取指定区域的图片
    region_image = pyautogui.screenshot(region=region_coords)
    # 使用imageShow()方法显示截取的图片
    region_image.show()

def cal_diff_between_regions(target_coords, main_region_coords):
    # 计算目标区域与主区域的坐标差值
    target_x, target_y, target_width, target_height = target_coords
    main_x, main_y, main_width, main_height = main_region_coords
    diff_x = target_x - main_x
    diff_y = target_y - main_y
    return (diff_x, diff_y, target_width, target_height)

def extract_int_from_image(image: np.ndarray, error_value: float) -> int:
    # 转为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 二值化
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # 去噪
    denoised = cv2.fastNlMeansDenoising(binary, h=10, templateWindowSize=7, searchWindowSize=21)
    # 缩放
    large = cv2.resize(denoised, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    # 使用pytesseract提取文字
    number_str = pytesseract.image_to_string(large, config='--psm 6 -c tessedit_char_whitelist=0123456789')
    number_str = "".join(filter(str.isdigit, re.findall(r'\d+', number_str)))
    if number_str == "":
        return error_value
    
    return int(number_str)