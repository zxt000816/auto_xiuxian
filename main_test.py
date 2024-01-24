import pyautogui
from utils_adb import *
from coords_manager import *

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True

main_region_coords = get_game_page_coords()
coor_manager = BaseCoordsManager(main_region_coords)

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
    'confidence': 0.95,
    'target_image_cat_dir': None,
}

get_diff_quickly = get_diff_quickly_2

diffs = get_diff_quickly(**args2)

# %% 
pyautogui.screenshot(region=diffs['target_image_coords'])
# %% 

diff_between_target_and_main = diffs['diff_between_target_and_main']

print("区域坐标为: ", diff_between_target_and_main)
print('中心坐标为: ',  calculate_center_coords(diff_between_target_and_main))

# %%