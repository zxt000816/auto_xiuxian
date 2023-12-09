import pyautogui
import numpy as np
from typing import Tuple
import time
from utils import get_game_page_coords
from coords_manager import YouliCoordsManager
from event_executor import YouLiExecutor

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True

main_region_coords = get_game_page_coords() # (x, y, width, height)

corrds_manager = YouliCoordsManager(main_region_coords)

youli_executor = YouLiExecutor(
    youli_coords_manager=corrds_manager,
    place_name='冰海', # 冰海 or 南疆
    buy_times=1
)

youli_executor.execute()
