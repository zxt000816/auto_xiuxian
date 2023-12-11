import time
import pyautogui
import numpy as np
import pandas as pd
from typing import Tuple
from utils import *
from coords_manager import BaseCoordsManager, GameControlCoordsManager
from event_executor import BaseExecutor, GameControlExecutor
from xiuxian_exception import *

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True
resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)

try:
    main_region_coords = get_game_page_coords(resolution = resolution)
except Exception as e:
    print(f"未定位到游戏界面!")

coords_manager = GameControlCoordsManager(main_region_coords)
account_name_ls = ['野菜花', '白起(仙山)', '白起(黄河)', '晴雪']

for account_name in account_name_ls:
    executor = GameControlExecutor(coords_manager, account_name=account_name)
    executor.execute()