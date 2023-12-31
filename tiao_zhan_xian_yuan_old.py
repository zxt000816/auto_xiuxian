import time
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

class TiaoZhanXianYuanCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)

    def all_xian_yuan(self):
        diff=(324, 280, 160, 80)
        return self.calculate_relative_coords(diff)
    
    def qian_wang(self):
        diff=(430, 1527, 255, 96)
        return self.calculate_relative_coords(diff)

class TiaoZhanXianYuanExecutor(BaseExecutor):
    def __init__(self, tzxy_coords_manager: TiaoZhanXianYuanCoordsManager, xian_yuan_role_name: str):
        super().__init__(tzxy_coords_manager, 'tiao_zhan_xian_yuan')
        self.tzxy_coords_manager = tzxy_coords_manager
        self.role_name_dict = {
            '尸魈': 'shi_xiao',
            '乌丑': 'wu_chou',
            '王婵': 'wang_chan',
            '极阴': 'ji_yin',
            '青背苍狼': 'qing_bei_cang_lang',
            '炫烨王': 'xuan_ye_wang',
            '黄枫灵鲲': 'huang_feng_ling_kun',
            '势不两立': 'shi_bu_liang_li'
        }
        self.candidate_role_names = ['势不两立', '尸魈', '炫烨王', '极阴', '王婵', '乌丑', '青背苍狼', '黄枫灵鲲']
        self.candidate_role_names.remove(xian_yuan_role_name)
        self.xian_yuan_role_name = xian_yuan_role_name
        self.xian_yuan_role = self.role_name_dict[xian_yuan_role_name]

    @wait_region
    def get_open_tiao_zhan_xian_yuan_coords(self, wait_time, target_region, is_to_click=False):
        tiao_zhan_xian_yuan_coords = get_region_coords(
            'open_tiao_zhan_xian_yuan',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir
        )
        return tiao_zhan_xian_yuan_coords
    
    @wait_region
    def get_jiao_ta_zuo_ren_coords(self, wait_time, target_region, is_to_click=False):
        jiao_ta_zuo_ren_coords = get_region_coords(
            'jiao_ta_zuo_ren',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
        return jiao_ta_zuo_ren_coords

    @wait_region
    def get_kan_zhao_ba_coords(self, wait_time, target_region, is_to_click=False):
        kan_zhao_ba_coords = get_region_coords(
            'kan_zhao_ba',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir,
        )
        return kan_zhao_ba_coords
    
    @wait_region
    def get_battle_over_coords(self, wait_time, target_region, is_to_click, wait_time_before_click):
        battle_over_coords = get_region_coords(
            'battle_over',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
        return battle_over_coords
    
    @wait_region
    def get_battle_over2_coords(self, wait_time, target_region, is_to_click, other_region_coords, wait_time_before_click):
        battle_over2_coords = get_region_coords(
            'battle_over2',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            grayscale=True,
            cat_dir=self.cat_dir,
        )
        return battle_over2_coords

    def execute(self, index=0):
        self.go_to_world()
        
        self.click_ri_chang()
        self.scoll_and_click(direction='down')

        # 确认`仙缘页面`是否打开
        self.get_open_tiao_zhan_xian_yuan_coords(wait_time=3, target_region='仙缘页面', is_to_click=False)
        click_region(self.tzxy_coords_manager.all_xian_yuan())

        try:
            self.scoll_and_click(
                direction='down', 
                other_target=self.xian_yuan_role, 
                other_target_name=self.xian_yuan_role_name, 
                confidence=0.8,
                num_of_scroll=10,
                scroll_length=400, 
                scroll_seconds=4
            )
        except Exception as e:
            print(f"没有{self.xian_yuan_role_name}!")
            self.xian_yuan_role_name = self.candidate_role_names[index]
            self.xian_yuan_role = self.role_name_dict[self.xian_yuan_role_name]
            print(f"切换为{self.xian_yuan_role_name}!")
            self.execute(index=index+1)
            
        click_region(self.tzxy_coords_manager.qian_wang())

        # 确认`教他做人`是否出现
        self.get_jiao_ta_zuo_ren_coords(wait_time=120, target_region='教他做人',is_to_click=True)

        # 确认`看招吧`是否出现
        self.get_kan_zhao_ba_coords(wait_time=10, target_region='看招吧', is_to_click=True)

        # 确认`战斗结束`是否出现
        self.get_battle_over_coords(wait_time=60, target_region='战斗结束', is_to_click=True, wait_time_before_click=2)

        # 确认`战斗结束2`是否出现
        self.get_battle_over2_coords(wait_time=20, target_region='战斗结束2', is_to_click=True, 
                                     other_region_coords=self.tzxy_coords_manager.exit(), wait_time_before_click=1)

if __name__ == '__main__':
    
    main_region_coords = get_game_page_coords(resolution = resolution)

    tzxy_coords_manager = TiaoZhanXianYuanCoordsManager(main_region_coords)
    executor = TiaoZhanXianYuanExecutor(tzxy_coords_manager, xian_yuan_role_name='势不两立')
    executor.execute()
