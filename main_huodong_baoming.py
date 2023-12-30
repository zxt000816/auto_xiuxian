import pyautogui
import numpy as np
from typing import Tuple
from utils import get_game_page_coords
from coords_manager import BaoMingCoordsManager
from event_executor import BaoMingExecutor

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True

main_region_coords = get_game_page_coords()
corrds_manager = BaoMingCoordsManager(main_region_coords)
executor = BaoMingExecutor(corrds_manager)

executor.execute()
