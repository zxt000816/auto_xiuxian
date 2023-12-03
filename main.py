import pyautogui
import numpy as np
from typing import Tuple
from utils import get_game_page_coords
from coords_manager import AssistantCoordsManager, BaoMingCoordsManager, YouliCoordsManager
from event_runner import AssistantExecutor, BaoMingExecutor, YouLiExecutor

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True

main_region_coords = get_game_page_coords()
assistant_corrds_manager = AssistantCoordsManager(main_region_coords)
bao_ming_corrds_manager = BaoMingCoordsManager(main_region_coords)
youli_corrds_manager = YouliCoordsManager(main_region_coords)

assistant_executor = AssistantExecutor(assistant_corrds_manager)
bao_ming_executor = BaoMingExecutor(bao_ming_corrds_manager)
youli_executor = YouLiExecutor(youli_corrds_manager, place_name='南疆', buy_times=2)

assistant_executor.execute()
bao_ming_executor.execute()
youli_executor.execute()
