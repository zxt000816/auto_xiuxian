import pyautogui
import numpy as np
from typing import Tuple
from utils import get_game_page_coords, get_region_coords, click_region, move_to_specific_coords, scroll_specific_length
from coords_manager import AssistantCoordsManager
from event_runner import AssistantExecutor

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True
    
main_region_coords = get_game_page_coords()
corrds_manager = AssistantCoordsManager(main_region_coords)
executor = AssistantExecutor(corrds_manager)

executor.execute()