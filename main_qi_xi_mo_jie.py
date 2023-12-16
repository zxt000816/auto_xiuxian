import time
import pyautogui
import numpy as np
from typing import Tuple
from utils import *
from coords_manager import QiXiMoJieCoordsManager
from event_executor import QiXiMoJieExecutor
from xiuxian_exception import *

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True
resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)

try:
    main_region_coords = get_game_page_coords(resolution = resolution)
except Exception as e:
    print(f"未定位到游戏界面!")

coords_manager = QiXiMoJieCoordsManager(main_region_coords)

executor = QiXiMoJieExecutor(coords_manager)

executor.execute()
