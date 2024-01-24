import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

import pyautogui
import numpy as np
from typing import Tuple
from utils_adb import get_game_page_coords, get_region_coords, click_region, get_game_page_coords, get_region_coords_by_multi_imgs
from coords_manager import  BaseCoordsManager
from event_executor import BaseExecutor

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True
resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)

try:
    main_region_coords = get_game_page_coords(resolution = resolution)
except Exception as e:
    print(f"未定位到游戏界面!")


class XiLingCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)

    def xilian_region(self):
        diff = (165, 1498, 312, 106)
        return self.calculate_relative_coords(diff)
    
    def xilian_results(self):
        diff = (542, 1008, 455, 347)
        return self.calculate_relative_coords(diff)
    
    def continue_xilian(self):
        diff = (210, 1220, 315, 110)
        return self.calculate_relative_coords(diff)
    

class XiLingExecutor(BaseExecutor):
    def __init__(self, xi_ling_coords_manager: XiLingCoordsManager):
        super().__init__(xi_ling_coords_manager, 'xi_ling')
        self.xi_ling_coords_manager = xi_ling_coords_manager
    
    def get_ling_qi_wu_shuang_coords(self):
        xi_lian_results_coords = self.xi_ling_coords_manager.xilian_results()
        ling_qi_wu_shuang_imgs = [
            {'target_region_image': 'ling_qi_wu_shuang_1', 'main_region_coords': xi_lian_results_coords, 'confidence': 0.4, 'grayscale': False, 'cat_dir': 'xi_ling'},
            {'target_region_image': 'ling_qi_wu_shuang_2', 'main_region_coords': xi_lian_results_coords, 'confidence': 0.4, 'grayscale': False, 'cat_dir': 'xi_ling'},
        ]

        ling_qi_wu_shuang_coords = get_region_coords_by_multi_imgs(ling_qi_wu_shuang_imgs)
        return ling_qi_wu_shuang_coords
    
    def get_high_level_attribute_alert_coords(self):
        high_level_attribute_alert_coords = get_region_coords(
            'high_level_attribute_alert',
            main_region_coords=self.xi_ling_coords_manager.main_region_coords,
            confidence=0.8,
            cat_dir='xi_ling',
        )
        return high_level_attribute_alert_coords

    def execute(self):
        # 假设处于洗灵页面
        while True:
            click_region(self.xi_ling_coords_manager.xilian_region(), seconds=0.2)
            ling_qi_wu_shuang_coords = self.get_ling_qi_wu_shuang_coords()

            if ling_qi_wu_shuang_coords:
                print("成功洗出灵器无双属性！")
                break
            
            high_level_attribute_alert_coords = self.get_high_level_attribute_alert_coords()
            if high_level_attribute_alert_coords:
                click_region(self.xi_ling_coords_manager.continue_xilian(), seconds=1)
                continue
            

xi_ling_coords_manager = XiLingCoordsManager(main_region_coords, resolution)
xi_ling_executor = XiLingExecutor(xi_ling_coords_manager)

xi_ling_executor.execute()