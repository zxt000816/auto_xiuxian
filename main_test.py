# import pyautogui, os

# resolution = (540, 960) # (width, height): (554, 984) or (1080, 1920)

# device_idx = input('请输入模拟器序号(1: 都有3, 2: 都有4, 3: 都有5): ')
# if device_idx == '1':
#     device_serial = 'emulator-5566' # '都有3'
# elif device_idx == '2':
#     device_serial = 'emulator-5568' # '都有4'
# elif device_idx == '3':
#     device_serial = 'emulator-5570' # '都有5'

# main_region_coords_dt = {
#     'emulator-5566': '1344,46,540,960',
# }

# # 添加环境变量
# os.environ['ROOT_DIR'] = f'FanRenXiuXianIcon_{resolution[0]}_{resolution[1]}'
# os.environ['DEVICE_SERIAL'] = device_serial
# os.environ['MAIN_REGION_COORDS'] = main_region_coords_dt[device_serial]

from utils_adb import *
from coords_manager import BaseCoordsManager
from event_executor import BaseExecutor

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True

# resolution = (540, 960)
# os.environ['ROOT_DIR'] = f'FanRenXiuXianIcon_{resolution[0]}_{resolution[1]}'
# main_region_coords = get_game_page_coords(resolution)

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
    'target_image_cat_dir': 'bai_zu_gong_feng',
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