import pyautogui
import numpy as np
from typing import Tuple
import time
from utils import *
from coords_manager import ShuangXiuCoordsManager
from event_runner import ShuangXiuExecutor
from xiuxian_exception import *

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True
        
main_region_coords = get_game_page_coords()
coords_manager = ShuangXiuCoordsManager(main_region_coords)
main_region_coords = coords_manager.main_region_coords

sx_executor = ShuangXiuExecutor(coords_manager)

sx_executor.go_to_world()