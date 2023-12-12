import time
import pyautogui
import numpy as np
import pandas as pd
from typing import Tuple
from utils import *
from coords_manager import BaseCoordsManager, ZhuiMoGuCoordsManager
from event_executor import BaseExecutor, ZhuiMoGuExecutor
from xiuxian_exception import *

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True
resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)

try:
    main_region_coords = get_game_page_coords(resolution = resolution)
except Exception as e:
    print(f"未定位到游戏界面!")

coords_manager = ZhuiMoGuCoordsManager(main_region_coords)
executor = ZhuiMoGuExecutor(coords_manager, '法', max_level='化神-前期-十层')
executor.execute()
