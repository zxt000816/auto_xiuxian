import time
import pyautogui
import numpy as np
from typing import Tuple
from utils import get_game_page_coords, get_region_coords, get_region_coords_by_multi_imgs, click_region, \
                  move_to_specific_coords, scroll_specific_length, extract_int_from_image
from coords_manager import BaseCoordsManager, BaiYeCoordsManager
from event_executor import BaseExecutor, BaiYeExecutor
from xiuxian_exception import *

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True
resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)

try:
    main_region_coords = get_game_page_coords(resolution = resolution)
except Exception as e:
    print(f"未定位到游戏界面!")

coords_manager = BaiYeCoordsManager(main_region_coords)
executor = BaiYeExecutor(coords_manager, event_name='魔道', fa_ze_level=1)
executor.execute()
