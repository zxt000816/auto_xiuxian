import time
import pyautogui
import numpy as np
from typing import Tuple
from utils import get_game_page_coords, get_region_coords, click_region, move_to_specific_coords, scroll_specific_length
from coords_manager import BaseCoordsManager, TiaoZhanXianYuanCoordsManager
from event_executor import BaseExecutor, TiaoZhanXianYuanExecutor
from xiuxian_exception import *

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True
resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)

try:
    main_region_coords = get_game_page_coords(resolution = resolution)
except Exception as e:
    print(f"未定位到游戏界面!")

tzxy_coords_manager = TiaoZhanXianYuanCoordsManager(main_region_coords)
executor = TiaoZhanXianYuanExecutor(tzxy_coords_manager, xian_yuan_role_name='王婵')
executor.execute()
