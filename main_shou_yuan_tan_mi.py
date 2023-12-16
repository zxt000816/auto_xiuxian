import time
import pyautogui
import numpy as np
from typing import Tuple
from utils import *
from swy_coords_manager import ShouYuanTanMiCoordsManager
from swy_event_executor import ShouYuanTanMiExecutor
from xiuxian_exception import *

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True
resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)

try:
    main_region_coords = get_game_page_coords(resolution = resolution)
except Exception as e:
    print(f"未定位到游戏界面!")

coords_manager = ShouYuanTanMiCoordsManager(main_region_coords)
executor = ShouYuanTanMiExecutor(coords_manager, server_nums=2, only_use_free_times=True)

executor.execute()
