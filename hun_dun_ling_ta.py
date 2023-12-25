import pyautogui
import numpy as np
from typing import Tuple
from utils import *
from coords_manager import HunDunLingTaCoordsManager, BaseCoordsManager
from event_executor import HunDunLingTaExecutor, BaseExecutor
import time

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True
resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)

try:
    main_region_coords = get_game_page_coords(resolution = resolution)
except Exception as e:
    print(f"未定位到游戏界面!")

class HunDunLingTaCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)

class HunDunLingTaExecutor(BaseExecutor):
    def __init__(self, hun_dun_ling_ta_coords_manager: HunDunLingTaCoordsManager, ling_ta_name: str):
        super().__init__(hun_dun_ling_ta_coords_manager, 'hun_dun_ling_ta')
        self.hun_dun_ling_ta_coords_manager = hun_dun_ling_ta_coords_manager
        self.ling_ta_name_dict = {
            '弥罗之塔': 'mi_luo_zhi_ta',
            '天月之塔': 'tian_yue_zhi_ta',
            '摩诃之塔': 'mo_he_zhi_ta',
        }
        self.ling_ta = self.ling_ta_name_dict[ling_ta_name]

    @wait_region
    def get_open_indicator_coords(self, wait_time, target_region):
        ling_ta_open_indicator_coords = get_region_coords(
            'open_indicator',
            main_region_coords=self.hun_dun_ling_ta_coords_manager.main_region_coords,
            confidence=0.8,
            cat_dir='hun_dun_ling_ta',
        )
        return ling_ta_open_indicator_coords
    
    @wait_region
    def get_sweep_coords(self, wait_time, target_region):
        sweep_coords = get_region_coords(
            'sweep',
            main_region_coords=self.hun_dun_ling_ta_coords_manager.main_region_coords,
            confidence=0.8,
            cat_dir='hun_dun_ling_ta',
        )
        return sweep_coords
    
    @wait_region
    def get_start_sweep_coords(self, wait_time, target_region):
        start_sweep_coords = get_region_coords(
            'start_sweep',
            main_region_coords=self.hun_dun_ling_ta_coords_manager.main_region_coords,
            confidence=0.8,
            cat_dir='hun_dun_ling_ta',
        )
        return start_sweep_coords
    
    def get_sweep_over_coords(self):
        sweep_over_coords = get_region_coords(
            'sweep_over',
            main_region_coords=self.hun_dun_ling_ta_coords_manager.main_region_coords,
            confidence=0.8,
            cat_dir='hun_dun_ling_ta',
        )
        return sweep_over_coords

    def execute(self):
        self.go_to_world()
        
        try:
            self.click_ri_chang()
            self.scoll_and_click(direction='down')

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
        
        except Exception as e:
            print(e)
            
        self.go_to_world()

corrds_manager = HunDunLingTaCoordsManager(main_region_coords)
executor = HunDunLingTaExecutor(corrds_manager, ling_ta_name='弥罗之塔')

executor.execute()
