import pyautogui
import numpy as np
from typing import Tuple
from utils import *
from coords_manager import BaseCoordsManager
from event_executor import BaseExecutor

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True

class BaoMingCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords: tuple, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)
    
    def baoming_region(self):
        diff = (827, 239, 150, 1438)
        return self.calculate_relative_coords(diff)
    
    def baoming_lingshi(self):
        diff = (398, 1233, 303, 101)
        return self.calculate_relative_coords(diff)

class BaoMingExecutor(BaseExecutor):
    def __init__(self, baoming_coords_manager: BaoMingCoordsManager):
        super().__init__(baoming_coords_manager, 'huodong_baoming')
        self.baoming_coords_manager = baoming_coords_manager

    def click_huo_dong_bao_ming(self):
        click_region(self.coords_manager.huo_dong_bao_ming(), seconds=3)
        print("完成: 点击报名按钮")
        x, y = list(self.coords_manager.scroll_start_point())[:2]
        move_to_specific_coords((x, y), seconds=1)
    
    def start_baoming(self):
        baoming_region_coords = self.baoming_coords_manager.baoming_region()
        get_baoming_coords_args = {
            'target_region_image': 'baoming',
            'main_region_coords': baoming_region_coords, 
            'confidence': 0.5, 
            'grayscale': False,
            'cat_dir': self.cat_dir
        }

        num_to_scroll = 2
        scroll_length = self.calculate_scroll_length(-300)

        while True:
            baoming_coords = get_region_coords(**get_baoming_coords_args)
            if baoming_coords is None:
                if num_to_scroll == 0:
                    break
                num_to_scroll -= 1

                scroll_specific_length(scroll_length, seconds=4)
                continue
                
            click_region(baoming_coords, seconds=2)
            print("完成: 点击报名按钮")
            click_region(self.baoming_coords_manager.baoming_lingshi(), seconds=2)
            print("完成: 完成报名按钮")
        
        print("完成: 报名")

    def execute(self):
        self.go_to_world()

        try:
            self.click_ri_chang()
            self.click_huo_dong_bao_ming()
            self.start_baoming()
        except Exception as e:
            print(e)

        self.go_to_world()

if __name__ == "__main__":

    main_region_coords = get_game_page_coords()

    corrds_manager = BaoMingCoordsManager(main_region_coords)
    
    executor = BaoMingExecutor(corrds_manager)

    executor.execute()
