
import time
import pyautogui
import numpy as np
from typing import Tuple
from utils_adb import *
from coords_manager import BaseCoordsManager
from event_executor import BaseExecutor
from xiuxian_exception import *

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True

class BaiYeCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)

    def drag_from(self):
        diff = (804, 1312, 0, 0)
        return self.calculate_relative_coords(diff)
    
    def drag_to(self):
        diff = (504, 1312, 0, 0)
        return self.calculate_relative_coords(diff)
    
    def san_qian_da_dao(self):
        diff = (144, 1538, 118, 110)
        return self.calculate_relative_coords(diff)

class BaiYeExecutor(BaseExecutor):
    def __init__(self, by_coords_manager: BaiYeCoordsManager, event_name: str, fa_ze_level=1):
        super().__init__(by_coords_manager, 'bai_ye')
        if event_name not in ['兽渊', '魔道', '云梦', '虚天殿', '天地奕局']:
            raise Exception('活动名字错误!')
        
        self.by_coords_manager = by_coords_manager
        self.event_name = event_name
        self.event_name_dict = {
            '兽渊': 'shou_yuan',
            '魔道': 'mo_dao',
            '云梦': 'yun_meng',
            '虚天殿': 'huan_xu',
            '天地奕局': 'xian_yi',
        }
        self.event = self.event_name_dict[self.event_name]
        self.fa_ze_level = fa_ze_level

    @wait_region
    def get_fa_ze_coords(self, wait_time, target_region, is_to_click, click_wait_time, to_raise_exception):
        return get_region_coords(
            'fa_ze',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )

    @drag_region
    def get_event_coords(self, wait_time, target_region, is_to_click, drag_from_coords, drag_to_coords):
        event_imgs = [
            {'target_region_image': f'{self.event}1', 'main_region_coords': self.main_region_coords, 'confidence': 0.8, 'cat_dir': self.cat_dir},
            {'target_region_image': f'{self.event}2', 'main_region_coords': self.main_region_coords, 'confidence': 0.8, 'cat_dir': self.cat_dir},
        ]
        event_coords = get_region_coords_by_multi_imgs(event_imgs)
        return event_coords
    
    @wait_region
    def get_bai_ye_start_coords(self, wait_time, target_region, is_to_click):
        bai_ye_start_coords = get_region_coords(
            'bai_ye_start',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
        return bai_ye_start_coords
    
    def get_bai_ye_over_coords(self):
        bai_ye_over_coords = get_region_coords(
            'bai_ye_over',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
        return bai_ye_over_coords

    def execute(self):
        self.go_to_world()

        # self.click_ri_chang()
        # self.scroll_and_click(direction='down')

        self.get_gong_fa_shu_icon_coords(wait_time=3, target_region='功法书图标', is_to_click=True, click_wait_time=3, to_raise_exception=True)

        self.get_fa_ze_coords(wait_time=3, target_region='法则', is_to_click=True, click_wait_time=3, to_raise_exception=True)

        click_region(self.by_coords_manager.san_qian_da_dao(), seconds=3)

        self.scroll_and_click(
            direction='down',
            other_target=f'{self.fa_ze_level}_kua_fa_ze',
            other_target_name=f'{self.fa_ze_level}跨法则',
            confidence=0.8,
            grayscale=False,
        )

        self.get_event_coords(
            wait_time=120, 
            target_region=self.event_name, 
            is_to_click=True, 
            drag_from_coords=self.by_coords_manager.drag_from(), 
            drag_to_coords=self.by_coords_manager.drag_to()
        )

        bai_ye_over_coords = self.get_bai_ye_over_coords()
        if bai_ye_over_coords:
            print('已拜谒!')
            return
        
        self.get_bai_ye_start_coords(wait_time=10, target_region='开始拜谒', is_to_click=True)

        bai_ye_over_coords = self.get_bai_ye_over_coords()
        if bai_ye_over_coords:
            print('已拜谒!')
            return

if __name__ == '__main__':
    
    resolution = (1080, 1920)

    main_region_coords = get_game_page_coords(resolution = resolution)

    coords_manager = BaiYeCoordsManager(main_region_coords)

    executor = BaiYeExecutor(coords_manager, event_name='兽渊', fa_ze_level=1)

    executor.execute()
