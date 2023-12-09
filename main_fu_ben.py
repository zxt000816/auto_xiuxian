import pyautogui
import numpy as np
from typing import Tuple
from utils import *
from coords_manager import FuBenCoordsManager
from event_executor import FuBenExecutor

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True
resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)

try:
    main_region_coords = get_game_page_coords(resolution = resolution)
except Exception as e:
    print(f"未定位到游戏界面!")

coords_manager = FuBenCoordsManager(main_region_coords)
main_region_coords = coords_manager.main_region_coords

fuben_executor = FuBenExecutor(coords_manager, '昆吾山', buy_times=2)
fuben_executor.execute()