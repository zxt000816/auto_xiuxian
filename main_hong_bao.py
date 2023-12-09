import pyautogui
import numpy as np
from typing import Tuple
from utils import get_game_page_coords, get_region_coords, get_region_coords_by_multi_imgs, click_region
from coords_manager import HongBaoCoordsManager
from event_executor import HongBaoExecutor

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True
resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)

try:
    main_region_coords = get_game_page_coords(resolution = resolution)
except Exception as e:
    print(f"未定位到游戏界面!")

hong_bao_coords_manager = HongBaoCoordsManager(main_region_coords, resolution=resolution)
hong_bao_executor = HongBaoExecutor(hong_bao_coords_manager)

hong_bao_executor.execute()