import pyautogui
import numpy as np
from typing import Tuple
from utils import *
from coords_manager import BaseCoordsManager
from event_executor import BaseExecutor
import time

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True
resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)


class HunDunLingTaCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)

class HunDunLingTaExecutor(BaseExecutor):
    def __init__(self, hdlt_cm: HunDunLingTaCoordsManager, ling_ta_name: str):
        super().__init__(hdlt_cm, 'hun_dun_ling_ta')
        self.hdlt_cm = hdlt_cm
        self.ling_ta_name_dict = {
            '弥罗之塔': 'mi_luo_zhi_ta',
            '天月之塔': 'tian_yue_zhi_ta',
            '摩诃之塔': 'mo_he_zhi_ta',
            '鸿古之塔': 'hong_gu_zhi_ta'
        }
        self.ling_ta_name = ling_ta_name
        self.ling_ta = self.ling_ta_name_dict[ling_ta_name]

    @wait_region
    def get_open_indicator_coords(self, wait_time, target_region):
        return get_region_coords(
            'open_indicator',
            main_region_coords=self.hdlt_cm.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_sweep_coords(self, wait_time, target_region):
        return get_region_coords(
            'sweep',
            main_region_coords=self.hdlt_cm.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_start_sweep_coords(self, wait_time, target_region):
        return get_region_coords(
            'start_sweep',
            main_region_coords=self.hdlt_cm.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
    
    def get_sweep_over_coords(self):
        return get_region_coords(
            'sweep_over',
            main_region_coords=self.hdlt_cm.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_tong_guan_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'tong_guan',
            main_region_coords=self.hdlt_cm.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_tiao_zhan_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'tiao_zhan',
            main_region_coords=self.hdlt_cm.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_tiao_zhan_over_coords(self, wait_time, target_region, is_to_click, other_region_coords, wait_time_before_click, to_raise_exception):
        tiao_zhan_over_imgs = [
            {'target_region_image': 'tiao_zhan_over1', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': self.cat_dir},
            {'target_region_image': 'tiao_zhan_over2', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': self.cat_dir},
            {'target_region_image': 'tiao_zhan_over3', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': self.cat_dir},
            {'target_region_image': 'tiao_zhan_over4', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': self.cat_dir},
        ]

        return get_region_coords_by_multi_imgs(tiao_zhan_over_imgs)
    
    @wait_region
    def get_next_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'next',
            main_region_coords=self.hdlt_cm.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_no_times_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'no_times',
            main_region_coords=self.hdlt_cm.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_dian_ji_ji_xu_coords(self, wait_time, target_region, is_to_click, wait_time_before_click, to_raise_exception):
        return get_region_coords(
            'dian_ji_ji_xu',
            main_region_coords=self.hdlt_cm.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir,
        )

    def go_up(self):
        self.go_to_world()

        self.click_ri_chang()
        self.scroll_and_click(direction='down', in_ri_chang_page=False)

        # 确认`混沌灵塔`是否打开
        self.get_open_indicator_coords(wait_time=120, target_region='混沌灵塔')

        self.scroll_and_click(
            direction='down',
            other_target=self.ling_ta,
            other_target_name=self.ling_ta_name,
            confidence=0.7,
            num_of_scroll=3,
            scroll_seconds=3,
            cat_dir=self.cat_dir,
        )

        no_times_coords = self.get_no_times_coords(wait_time=5, target_region='没有次数', is_to_click=True, to_raise_exception=False)
        if no_times_coords is not None:
            raise Exception(f"没有{self.ling_ta_name}次数!")

        tong_tuan_coords = self.get_tong_guan_coords(wait_time=5, target_region='通关', is_to_click=False, to_raise_exception=False)
        if tong_tuan_coords is not None:
            raise Exception(f"已经通关{self.ling_ta_name}!")
        
        self.get_tiao_zhan_coords(wait_time=5, target_region='挑战', is_to_click=True, to_raise_exception=True)
        
        start_time = time.time()
        while True:
            if time.time() - start_time > 600:
                raise Exception(f"挑战{self.ling_ta_name}超时!")
            
            tiao_zhan_over_coords = self.get_tiao_zhan_over_coords(wait_time=2, target_region='挑战结束', is_to_click=True, 
                                                                   other_region_coords=self.hdlt_cm.exit(), wait_time_before_click=4, 
                                                                   to_raise_exception=False)
            if tiao_zhan_over_coords is not None:
                break

            self.get_next_coords(wait_time=2, target_region='下一关', is_to_click=True, to_raise_exception=False)

    def sao_dang(self):
        self.go_to_world()
        
        self.click_ri_chang()
        self.scroll_and_click(direction='down', in_ri_chang_page=False)

        # 确认`混沌灵塔`是否打开
        self.get_open_indicator_coords(wait_time=120, target_region='混沌灵塔')

        # 点击混沌灵塔界面的扫荡按钮
        sweep_coords = self.get_sweep_coords(wait_time=10, target_region='扫荡')
        click_region(sweep_coords)

        # 如果弹出扫荡完成界面, 则返回世界
        sweep_over_coords = self.get_sweep_over_coords()
        if sweep_over_coords is None:
            # 如果没有弹出扫荡完成界面, 则点击开始扫荡
            start_sweep_coords = self.get_start_sweep_coords(wait_time=10, target_region='开始扫荡')
            click_region(start_sweep_coords)
            
            # 跳过动画
            time.sleep(1)
            click_region(self.hdlt_cm.exit())

            self.get_dian_ji_ji_xu_coords(wait_time=10, target_region='点击继续', is_to_click=True, 
                                          wait_time_before_click=6, to_raise_exception=False)

if __name__ == '__main__':
    
    main_region_coords = get_game_page_coords(resolution = resolution)

    corrds_manager = HunDunLingTaCoordsManager(main_region_coords)
    executor = HunDunLingTaExecutor(corrds_manager, ling_ta_name='鸿古之塔')
    
    executor.go_up()
    executor.sao_dang()
