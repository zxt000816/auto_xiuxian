import pyautogui
import numpy as np
from typing import Tuple
from utils import get_game_page_coords, get_region_coords, click_region, move_to_specific_coords, scroll_specific_length
from coords_manager import HunDunLingTaCoordsManager
from event_runner import HunDunLingTaExecutor
import time

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True
resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)

try:
    main_region_coords = get_game_page_coords(resolution = resolution)
except Exception as e:
    print(f"未定位到游戏界面!")

corrds_manager = HunDunLingTaCoordsManager(main_region_coords)
executor = HunDunLingTaExecutor(corrds_manager, ling_ta_name='弥罗之塔')

executor.execute()
