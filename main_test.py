import os
import adbutils

adb = adbutils.AdbClient(host="127.0.0.1", port=5037)

serial = "emulator-5566"
device = adb.device(serial=serial)

resolution = (540, 960)
os.environ['DEVICE_SERIAL'] = serial
os.environ['ROOT_DIR'] = f'FanRenXiuXianIcon_{resolution[0]}_{resolution[1]}'

main_region_coords = (1364, 47, 540, 960)

os.environ['MAIN_REGION_COORDS'] = ','.join(map(str, main_region_coords))

import pyautogui
from utils_adb import get_region_coords, wait_region, click_region, cal_diff_between_regions, calculate_center_coords
from coords_manager import BaseCoordsManager
from event_executor import BaseExecutor

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True

coor_manager = BaseCoordsManager(main_region_coords)
executor = BaseExecutor(coor_manager)

def get_diff_quickly_2(
    target_image_name: str,
    main_region_coords: tuple,
    confidence: float = 0.9,
    target_image_cat_dir: str = None,
) -> tuple:
    target_image_coords = get_region_coords(
        target_image_name,
        main_region_coords=main_region_coords,
        confidence=confidence,
        cat_dir=target_image_cat_dir,
    )

    diff_between_target_and_main = cal_diff_between_regions(
        target_image_coords,
        main_region_coords,
    )

    return {
        'target_image_coords': target_image_coords,
        'main_region_coords': main_region_coords,
        'diff_between_target_and_main': diff_between_target_and_main,
    }

def get_diff_quickly_3(
    target_image_name: str,
    sub_main_image_name: str,
    main_region_coords: tuple,
    target_image_cat_dir: str = None,
    sub_main_image_cat_dir: str = None,
) -> tuple:
    sub_main_image_coords = get_region_coords(
        sub_main_image_name,
        main_region_coords=main_region_coords,
        confidence=0.9,
        cat_dir=sub_main_image_cat_dir,
    )

    target_image_coords = get_region_coords(
        target_image_name,
        main_region_coords=sub_main_image_coords,
        confidence=0.9,
        cat_dir=target_image_cat_dir,
    )

    diff_between_sub_main_and_main = cal_diff_between_regions(
        sub_main_image_coords,
        main_region_coords,
    )

    diff_between_target_and_sub_main = cal_diff_between_regions(
        target_image_coords,
        sub_main_image_coords,
    )

    diff_between_target_and_main = cal_diff_between_regions(
        target_image_coords,
        main_region_coords,
    )

    return {
        'target_image_coords': target_image_coords,
        'sub_main_image_coords': sub_main_image_coords,
        'main_region_coords': main_region_coords,
        'diff_between_sub_main_and_main': diff_between_sub_main_and_main,
        'diff_between_target_and_sub_main': diff_between_target_and_sub_main,
        'diff_between_target_and_main': diff_between_target_and_main,
    }

args3 = {
    'target_image_name': 'baoming',
    'sub_main_image_name': 'baoming_region',
    'main_region_coords': main_region_coords,
    'target_image_cat_dir': 'assistant',
    'sub_main_image_cat_dir': 'assistant',
}

args2 = {
    'target_image_name': 'temp_test',
    'main_region_coords': main_region_coords,
    'confidence': 0.9,
    'target_image_cat_dir': 'wan_ling_qie_cuo',
}

get_diff_quickly = get_diff_quickly_2

diffs = get_diff_quickly(**args2)

target_image_coords = diffs['target_image_coords']
# change all elements in target_image_coords to int
target_image_coords = tuple(map(int, target_image_coords))

target_image_center_coords = calculate_center_coords(target_image_coords)

executor.cal_x_y_ratio(target_image_center_coords[0], target_image_center_coords[1])

# %% 
pyautogui.screenshot(region=target_image_coords)
# %% 

diff_between_target_and_main = diffs['diff_between_target_and_main']

print("区域坐标为: ", diff_between_target_and_main)
print('中心坐标为: ',  calculate_center_coords(diff_between_target_and_main))

# %%