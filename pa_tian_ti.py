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

class PaTianTiCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)

    def all_xian_yuan(self):
        diff=(324, 280, 160, 80)
        return self.calculate_relative_coords(diff)
    
class PaTianTiExecutor(BaseExecutor):
    def __init__(self, ptt_coords_manager: PaTianTiCoordsManager):
        super().__init__(ptt_coords_manager)
        self.ptt_coords_manager = ptt_coords_manager
        self.cat_dir = 'pa_tian_ti'

    @wait_region
    def get_open_tiao_zhan_xian_yuan_coords(self, wait_time, target_region, is_to_click=False):
        tiao_zhan_xian_yuan_coords = get_region_coords(
            'open_tiao_zhan_xian_yuan',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir
        )
        return tiao_zhan_xian_yuan_coords
    
    @wait_region
    def get_fei_sheng_coords(self, wait_time, target_region, is_to_click, click_wait_time, wait_time_before_click, to_raise_exception):
        fei_sheng_imgs = [
            {'target_region_image': 'fei_sheng1', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': True, 'cat_dir': self.cat_dir},
            {'target_region_image': 'fei_sheng2', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': True, 'cat_dir': self.cat_dir},
            {'target_region_image': 'fei_sheng3', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': True, 'cat_dir': self.cat_dir},
        ]
        return get_region_coords_by_multi_imgs(fei_sheng_imgs)

    @wait_region
    def get_deng_shang_tian_ti_coords(self, wait_time, target_region, is_to_click, click_wait_time, wait_time_before_click, to_raise_exception):
        return get_region_coords(
            'deng_shang_tian_ti',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir
        )
    
    @wait_region
    def get_deng_jie_coords(self, wait_time, target_region, is_to_click, click_wait_time, wait_time_before_click, to_raise_exception):
        return get_region_coords(
            'deng_jie',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir
        )
    
    @wait_region
    def get_tiao_guo_coords(self, wait_time, target_region, is_to_click, click_wait_time, wait_time_before_click, to_raise_exception):
        return get_region_coords(
            'tiao_guo',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            grayscale=True,
            cat_dir=self.cat_dir
        )
    
    @wait_region
    def get_ji_xu_coords(self, wait_time, target_region, is_to_click, click_wait_time, wait_time_before_click, to_raise_exception):
        return get_region_coords(
            'ji_xu',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir
        )
    
    @wait_region
    def get_confirm_coords(self, wait_time, target_region, is_to_click, click_wait_time, wait_time_before_click, to_raise_exception):
        return get_region_coords(
            'confirm',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir
        )
    
    @wait_region
    def get_xiu_wei_not_enough_coords(self, wait_time, target_region, is_to_click, click_wait_time, wait_time_before_click, to_raise_exception):
        return get_region_coords(
            'xiu_wei_not_enough',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir
        )

    def execute(self):
        
        self.go_to_world()

        self.click_ri_chang()
        self.scroll_and_click(direction='down', other_target='pa_tian_ti', other_target_name='爬天梯', cat_dir=self.cat_dir)

        self.get_deng_shang_tian_ti_coords(
            wait_time=3,
            target_region="登上天梯",
            is_to_click=True,
            click_wait_time=1,
            wait_time_before_click=1,
            to_raise_exception=True
        )

        while True:
            self.get_deng_jie_coords(
                wait_time=60,
                target_region="登阶",
                is_to_click=True,
                click_wait_time=1,
                wait_time_before_click=1,
                to_raise_exception=True
            )

            xiu_wei_not_enough_coords = self.get_xiu_wei_not_enough_coords(
                wait_time=2,
                target_region="修为不足",
                is_to_click=False,
                click_wait_time=0,
                wait_time_before_click=0,
                to_raise_exception=False
            )
            if xiu_wei_not_enough_coords is not None:
                print(f"修为不足!")
                break

            confirm_coords = self.get_confirm_coords(
                wait_time=2,
                target_region="确认",
                is_to_click=True,
                click_wait_time=1,
                wait_time_before_click=0,
                to_raise_exception=False
            )

            self.get_tiao_guo_coords(
                wait_time=5,
                target_region="跳过",
                is_to_click=True,
                click_wait_time=1,
                wait_time_before_click=0,
                to_raise_exception=True
            )

            ji_xu_wait_time = 5
            if confirm_coords is not None:
                ji_xu_wait_time = 200

            self.get_ji_xu_coords(
                wait_time=ji_xu_wait_time,
                target_region="继续",
                is_to_click=True,
                click_wait_time=1,
                wait_time_before_click=0,
                to_raise_exception=True
            )

if __name__ == '__main__':

    resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)

    main_region_coords = get_game_page_coords(resolution = resolution)

    ptt_coords_manager = PaTianTiCoordsManager(main_region_coords)
    executor = PaTianTiExecutor(ptt_coords_manager)
    executor.execute()
