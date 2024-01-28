import pyautogui
import os
import pytesseract
import re
import cv2
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

adb = adbutils.AdbClient(host="127.0.0.1", port=5037)

serial = os.getenv('DEVICE_SERIAL')
device = adb.device(serial=serial)

# resolution = os.getenv('RESOLUTION')
# resolution = resolution.split('x')
# resolution = (int(resolution[0]), int(resolution[1]))
# main_region_coords = get_game_page_coords(resolution)
main_region_coords = os.getenv('MAIN_REGION_COORDS')
main_region_coords = tuple(map(int, main_region_coords.split(',')))
print(f"获取游戏界面坐标: {main_region_coords}")
print(f"设备: {device}")

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

# def get_region_coords(
#     target_region_image, 
#     main_region_coords=None, 
#     confidence=0.7,
#     grayscale=False,
#     root_dir=os.getenv('ROOT_DIR'),
#     cat_dir=None
# ):
#     if cat_dir is not None:
#         root_dir = os.path.join(root_dir, cat_dir)

#     image_path = os.path.join(root_dir, f'{target_region_image}.png')
#     needle_image = image.imread(image_path)
#     needle_image = needle_image[:, :, ::-1]
#     haystack_image = np.array(device.screenshot()).astype(np.float32)

#     try:
#         # 在登录页面区域内定位指定区域的坐标
#         if main_region_coords is not None:
#             region_coords = pyautogui.locate(
#                 needle_image,
#                 haystack_image,
#                 confidence=confidence,
#                 grayscale=grayscale,
#                 region=main_region_coords
#             )
#         else:
#             region_coords = pyautogui.locate(
#                 needle_image,
#                 haystack_image,
#                 confidence=confidence,
#                 grayscale=grayscale
#             )
#     except ImageNotFoundException:
#         region_coords = None

#     return region_coords

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

def wait_for_evelen():
    hour = datetime.now().hour
    minute = datetime.now().minute

    if hour == 10 and minute > 45:
        wait_seconds = (60 - minute) * 60
        print(f'等待{wait_seconds}秒')
        time.sleep(wait_seconds)

def calculate_center_coords(coords: Tuple[int, int, int, int]) -> Tuple[int, int]:
        return (coords[0] + int(coords[2] / 2), coords[1] + int(coords[3] / 2))

def hide_yang_chong_tou(main_region_coords: Tuple[int, int, int, int], hidden_region_coords: Tuple[int, int]):
        
        yang_chong_tou_imgs = [
            {'target_region_image': 'yang_chong_tou1', 'main_region_coords': main_region_coords, 'confidence': 0.7, 'grayscale': False},
            {'target_region_image': 'yang_chong_tou2', 'main_region_coords': main_region_coords, 'confidence': 0.7, 'grayscale': False},
        ]

        yang_chong_tou_coords = get_region_coords_by_multi_imgs(yang_chong_tou_imgs)
        
        if yang_chong_tou_coords is None:
            return
        
        yang_chong_tou_center_coords = calculate_center_coords(yang_chong_tou_coords)

        pyautogui.moveTo(yang_chong_tou_center_coords[0], yang_chong_tou_center_coords[1])
        pyautogui.dragTo(hidden_region_coords, duration=2) 

        time.sleep(2)

        confirm_hide_yang_chong_tou_coords = get_region_coords(
            'confirm_hide_yang_chong_tou',
            main_region_coords,
            confidence=0.7,
        )
        click_region(confirm_hide_yang_chong_tou_coords, seconds=1)

def get_region_coords_by_multi_imgs(images: List[Dict]):
    # images: list of dict, example: [{'target_region_image': 'shouye', 'main_region_coords': (0, 0, 100, 100)}, ...]
    for image in images:
        target_region_image = image['target_region_image']
        main_region_coords = image.get('main_region_coords')
        confidence = image.get('confidence', 0.7)
        grayscale = image.get('grayscale', False)
        root_dir = image.get('root_dir', os.getenv('ROOT_DIR'))
        cat_dir = image.get('cat_dir')

        if cat_dir is not None:
            root_dir = os.path.join(root_dir, cat_dir)

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

        if region_coords is not None:
            print(f'定位到{target_region_image}')
            return region_coords

    return None

# def get_region_coords_by_multi_imgs(images: List[Dict]):
#     # images: list of dict, example: [{'target_region_image': 'shouye', 'main_region_coords': (0, 0, 100, 100)}, ...]
#     for image_dict in images:
#         target_region_image = image_dict['target_region_image']
#         main_region_coords = image_dict.get('main_region_coords')
#         confidence = image_dict.get('confidence', 0.7)
#         grayscale = image_dict.get('grayscale', False)
#         root_dir = image_dict.get('root_dir', os.getenv('ROOT_DIR'))
#         cat_dir = image_dict.get('cat_dir')

#         if cat_dir is not None:
#             root_dir = os.path.join(root_dir, cat_dir)

#         image_path = os.path.join(root_dir, f'{target_region_image}.png')
        
#         needle_image = image.imread(image_path)
#         needle_image = needle_image[:, :, ::-1]
#         haystack_image = np.array(device.screenshot()).astype(np.float32)

#         try:
#             # 在登录页面区域内定位指定区域的坐标
#             if main_region_coords is not None:
#                 region_coords = pyautogui.locate(
#                     needle_image,
#                     haystack_image,
#                     confidence=confidence,
#                     grayscale=grayscale,
#                     region=main_region_coords
#                 )
#             else:
#                 region_coords = pyautogui.locate(
#                     needle_image,
#                     haystack_image,
#                     confidence=confidence,
#                     grayscale=grayscale
#                 )
#         except ImageNotFoundException:
#             region_coords = None

#         if region_coords is not None:
#             print(f'定位到{target_region_image}')
#             return region_coords

#     return None

# def click_region(region_coords, button='left', seconds=2):
#     x, y = pyautogui.center(region_coords)
#     pyautogui.click(x, y, button=button)
#     time.sleep(seconds)

def click_region(
    region_coords, 
    button='left', 
    seconds=2, 
    # main_region_coords=(0, 0, 1080, 1920)
):
    x, y = pyautogui.center(region_coords)
    x = x - main_region_coords[0]
    y = y - main_region_coords[1]
    device.click(x, y)
    time.sleep(seconds)

def click_region_by_x_y(x, y, button='left'):
    pyautogui.click(x, y, button=button)

def scroll_specific_length(
    start_x: float,
    end_x: float,
    start_y: float,
    end_y: float,
    seconds: int = 3, 
    duration: float = 1.5,
    # main_region_coords: Tuple[int, int, int, int] = (0, 0, 1080, 1920)
):
    # minus length means scroll down
    # plus length means scroll up

    width = main_region_coords[2]
    height = main_region_coords[3]

    start_x = start_x * width
    start_x = int(round(start_x))

    end_x = end_x * width
    end_x = int(round(end_x))

    start_y = start_y * height
    start_y = int(round(start_y))

    end_y = end_y * height
    end_y = int(round(end_y))

    device.swipe(start_x, start_y, end_x, end_y, duration=duration)
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

def extract_int_from_image(image: np.ndarray, error_value: float = 3) -> int:
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

def click_if_coords_exist(func):
    def wrapper(self, *args, **kwargs):
        target_region = kwargs.get('target_region', None)
        to_raise_exception = kwargs.get('to_raise_exception', True)
        target_region_coords = func(self, *args, **kwargs)
        if target_region_coords is not None:
            click_region(target_region_coords)
            print(f"完成: 点击{target_region}!")
        else:
            if to_raise_exception:
                raise TargetRegionNotFoundException(f"未定位到{target_region}!")
            else:
                print(f"未定位到{target_region}!")
                return None
            
    return wrapper

def wait_region(func):
    def wrapper(self, *args, **kwargs):
        start_time = time.time()
        wait_time = kwargs.get('wait_time', 3)
        target_region = kwargs.get('target_region', None)
        is_to_click = kwargs.get('is_to_click', False)
        click_wait_time = kwargs.get('click_wait_time', 2)
        other_region_coords = kwargs.get('other_region_coords', None)
        to_raise_exception = kwargs.get('to_raise_exception', True)
        wait_time_before_click = kwargs.get('wait_time_before_click', 0)
        print(f"完成: 等待{wait_time}秒, 等待`{target_region}`出现...")
        while True:
            if time.time() - start_time > wait_time:
                if to_raise_exception:
                    raise TargetRegionNotFoundException(f"完成: 等待超时, `{target_region}`未出现!")
                else:
                    print(f"完成: 等待超时, `{target_region}`未出现!")
                    return None
            
            result_coords = func(self, *args, **kwargs)
            if result_coords:
                print(f"完成: `{target_region}`出现!")
                if is_to_click:
                    if other_region_coords:
                        time.sleep(wait_time_before_click)
                        click_region(other_region_coords, seconds=click_wait_time)
                    else:
                        time.sleep(wait_time_before_click)
                        click_region(result_coords, seconds=click_wait_time)
                        print(f"完成: 点击{target_region}!")
                    
                return result_coords

    return wrapper

def search_region(func):
    def wrapper(self, *args, **kwargs):
        start_time = time.time()
        wait_time = kwargs.get('wait_time', 3)
        target_region = kwargs.get('target_region', None)
        region_to_click = kwargs.get('region_to_click', None)
        region_to_click_name = kwargs.get('region_to_click_name', None)

        print(f"完成: 等待{wait_time}秒, 等待`{target_region}`出现...")
        while True:
            if time.time() - start_time > wait_time:
                raise TargetRegionNotFoundException(f"完成: 等待超时, `{target_region}`未出现!")
            
            result_coords = func(self, *args, **kwargs)
            if result_coords:
                print(f"完成: `{target_region}`出现!")
                return result_coords
            else:
                click_region(region_to_click, seconds=1)
                print(f"完成: 点击{region_to_click_name}!")

    return wrapper

def drag_to_specific_coords(start_coords, end_coords, duration=2):
    pyautogui.moveTo(start_coords[0], start_coords[1])
    pyautogui.dragTo(end_coords[0], end_coords[1], button='left', duration=duration)

def drag_region(func):
    def wrapper(self, *args, **kwargs):
        start_time = time.time()
        wait_time = kwargs.get('wait_time', 3)
        target_region = kwargs.get('target_region', None)
        is_to_click = kwargs.get('is_to_click', False)
        # drag_from_coords = kwargs.get('drag_from_coords', None)
        # drag_to_coords = kwargs.get('drag_to_coords', None)

        print(f"完成: 等待{wait_time}秒, 等待`{target_region}`出现...")
        while True:
            if time.time() - start_time > wait_time:
                raise TargetRegionNotFoundException(f"完成: 等待超时, `{target_region}`未出现!")
            
            result_coords = func(self, *args, **kwargs)
            if result_coords:
                print(f"完成: `{target_region}`出现!")
                if is_to_click:
                    click_region(result_coords)
                    print(f"完成: 点击`{target_region}`!")
                break
            else:
                # drag_to_specific_coords(drag_from_coords, drag_to_coords, duration=2)
                scroll_specific_length(
                    start_x=0.3,
                    end_x=0.7,
                    start_y=0.7,
                    end_y=0.7,
                    seconds=2
                )

    return wrapper

def wait_region_not_raise_exception(func):
    def wrapper(self, *args, **kwargs):
        start_time = time.time()
        wait_time = kwargs.get('wait_time', 3)
        target_region = kwargs.get('target_region', None)
        is_to_click = kwargs.get('is_to_click', False)
        print(f"完成: 等待{wait_time}秒, 等待`{target_region}`出现...")
        while True:
            if time.time() - start_time > wait_time:
                return None
            
            result_coords = func(self, *args, **kwargs)
            if result_coords:
                print(f"完成: `{target_region}`出现!")
                if is_to_click:
                    click_region(result_coords)
                    print(f"完成: 点击{target_region}!")
                return result_coords

    return wrapper