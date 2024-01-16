import time
from datetime import datetime
import pyautogui
import numpy as np
from typing import Tuple
from utils import *
from coords_manager import BaseCoordsManager
from event_executor import BaseExecutor
from xiuxian_exception import *

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True
resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)

class UseDaoJuCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)

class UseDaoJuExecutor(BaseExecutor):
    def __init__(self, usdj_coords_manager: UseDaoJuCoordsManager):
        super().__init__(usdj_coords_manager)
        self.usdj_coords_manager = usdj_coords_manager
        self.cat_dir = 'use_dao_ju'

    def execute(self):

        self.go_to_world()


if __name__ == '__main__':

    main_region_coords = get_game_page_coords(resolution = resolution)

    coords_manager = UseDaoJuCoordsManager(main_region_coords)
    executor = UseDaoJuExecutor(coords_manager)

    executor.execute()
