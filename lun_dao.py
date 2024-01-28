import time
import pyautogui
import numpy as np
import pandas as pd
from typing import Tuple
from utils_adb import *
from coords_manager import BaseCoordsManager
from event_executor import BaseExecutor
from xiuxian_exception import *

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True


class LunDaoCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)

    def ru_zuo_coords(self):
        diff = (839, 794, 128, 159)
        return self.calculate_relative_coords(diff)
    
    def leave_dao_chang_coords(self):
        diff = (930, 872, 103, 131)
        return self.calculate_relative_coords(diff)
        
class LunDaoExecutor(BaseExecutor):
    def __init__(self, ld_coords_manager: LunDaoCoordsManager, dao_chang_level: int):
        super().__init__(ld_coords_manager, 'lun_dao')
        self.ld_coords_manager = ld_coords_manager
        self.dao_chang_level = dao_chang_level
        self.dao_change_name_dict = {1: '大罗道场', 2: '三清道场',3: '御界道场',4: '耀星道场'}
        self.dao_chang_name = self.dao_change_name_dict[dao_chang_level]

    @wait_region
    # def get_ru_zuo_coords(self, wait_time, target_region, is_to_click, other_region_coords, to_raise_exception):
    def get_ru_zuo_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'ru_zuo',
            main_region_coords=self.main_region_coords,
            confidence=0.9,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_confirm_in_ru_zuo_alert_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'confirm_in_ru_zuo_alert',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_sit_down_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'sit_down',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_confirm_in_sit_down_alert_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'confirm_in_sit_down_alert',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_lun_dao_over_coords(self, wait_time, target_region, is_to_click, wait_time_before_click, to_raise_exception):
        return get_region_coords(
            'lun_dao_over',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_confirm_in_lun_dao_over_alert_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'confirm_in_lun_dao_over_alert',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_confirm_leave_dao_chang_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'confirm_leave_dao_chang',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_wen_dao_ing_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        wen_dao_ing_imgs = [
            {'target_region_image': 'wen_dao_zhong1', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': self.cat_dir},
            {'target_region_image': 'wen_dao_zhong2', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': self.cat_dir},
            {'target_region_image': 'wen_dao_zhong3', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': self.cat_dir},
        ]
        return get_region_coords_by_multi_imgs(wen_dao_ing_imgs)
    
    @wait_region
    def get_lun_dao_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'lun_dao',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )

    def execute(self):
        self.go_to_world()

        click_region(self.ld_coords_manager.ri_cheng())
        self.get_general_coords(wait_time=5, target_region='常规', is_to_click=True, to_raise_exception=True)

        self.get_lun_dao_coords(wait_time=5, target_region='论道', is_to_click=True, to_raise_exception=True)

        wen_dao_ing_coords = self.get_wen_dao_ing_coords(wait_time=5, target_region='问道中', is_to_click=False, to_raise_exception=False)
        if wen_dao_ing_coords:
            print('正在论道中!')
            return

        self.scroll_and_click(
            direction='down',
            other_target=f'dao_chang{self.dao_chang_level}',
            other_target_name=self.dao_chang_name,
            confidence=0.9,
            num_of_scroll=2,
            scroll_seconds=2,
            grayscale=False,
            cat_dir=self.cat_dir,
            in_ri_chang_page=False,
            is_to_click=True,
        )

        self.get_ru_zuo_coords(
            wait_time=5,
            target_region='空座位',
            is_to_click=True,
            # other_region_coords=self.ld_coords_manager.ru_zuo_coords(),
            to_raise_exception=True,
        )

        self.get_confirm_in_ru_zuo_alert_coords(
            wait_time=5,
            target_region='确认入座',
            is_to_click=True,
            to_raise_exception=True,
        )

        self.get_sit_down_coords(
            wait_time=30,
            target_region='坐下',
            is_to_click=True,
            to_raise_exception=True,
        )

        self.get_confirm_in_sit_down_alert_coords(
            wait_time=5,
            target_region='确认坐下',
            is_to_click=True,
            to_raise_exception=True,
        )

        self.get_lun_dao_over_coords(
            wait_time=5,
            target_region='论道结束',
            is_to_click=True,
            wait_time_before_click=2,
            to_raise_exception=True,
        )

        self.get_confirm_in_lun_dao_over_alert_coords(
            wait_time=5,
            target_region='确认论道结束',
            is_to_click=True,
            to_raise_exception=True,
        )

        time.sleep(3)

        click_region(self.ld_coords_manager.leave_dao_chang_coords())

        self.get_confirm_leave_dao_chang_coords(
            wait_time=5,
            target_region='确认离开道场',
            is_to_click=True,
            to_raise_exception=True,
        )

if __name__ == '__main__':

    resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)

    main_region_coords = get_game_page_coords(resolution = resolution)

    coords_manager = LunDaoCoordsManager(main_region_coords)
    executor = LunDaoExecutor(coords_manager, dao_chang_level=3)

    executor.execute()
