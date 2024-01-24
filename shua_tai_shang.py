import time
from datetime import datetime
import pyautogui
import numpy as np
from typing import Tuple
from utils_adb import *
from coords_manager import BaseCoordsManager
from event_executor import BaseExecutor
from mo_dao_ru_qing import MoDaoRuQingCoordsManager, MoDaoRuQingExecutor
from xiuxian_exception import *

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True

class ShuaTaiShangCoordsManager(MoDaoRuQingCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)

class ShuaTaiShangExecutor(MoDaoRuQingExecutor):
    def __init__(self, sts_cm: ShuaTaiShangCoordsManager):
        super().__init__(sts_cm, server_nums=1)
        self.sts_cm = sts_cm
        self.cat_dir = 'mo_dao_ru_qing'

    def execute(self):
        while True:
            self.get_tan_cha_coords(wait_time=2, target_region="探查", is_to_click=True, to_raise_exception=True)

            tan_cha_over_coords = self.get_tan_cha_over(
                wait_time=2, target_region="探查结束", is_to_click=True, 
                other_region_coords=self.mdrq_coords_manager.exit(), to_raise_exception=False
            )
            if tan_cha_over_coords is not None:
                print(f"探查结束!")
                break

            self.get_confirm_tan_cha(wait_time=5, target_region="确认探查", is_to_click=True, to_raise_exception=True)

if __name__ == '__main__':
    resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)

    main_region_coords = get_game_page_coords(resolution = resolution)

    coords_manager = ShuaTaiShangCoordsManager(main_region_coords)
    executor = ShuaTaiShangExecutor(coords_manager)

    executor.execute()

