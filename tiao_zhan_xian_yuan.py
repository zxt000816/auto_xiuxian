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
    def __init__(self, tzxy_coords_manager: TiaoZhanXianYuanCoordsManager, xian_yuan_role_name: str, wei_mian: str='人界'):
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
        self.wei_mian = wei_mian

    @wait_region
    def get_tzxy_icon_coords(self, wait_time, target_region, is_to_click, click_wait_time, to_raise_exception):
        tzxy_icon_imgs = [
            {'target_region_image': 'tzxy_icon1', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': self.cat_dir},
            {'target_region_image': 'tzxy_icon2', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': self.cat_dir},
        ]
        return get_region_coords_by_multi_imgs(tzxy_icon_imgs)

    @wait_region
    def get_open_tiao_zhan_xian_yuan_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
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
    
    @wait_region
    def get_ling_jie_coords(self, wait_time, target_region, is_to_click, wait_time_before_click, to_raise_exception):
        return get_region_coords(
            'ling_jie',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_ren_jie_coords(self, wait_time, target_region, is_to_click, wait_time_before_click, to_raise_exception):
        return get_region_coords(
            'ren_jie',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )

    def execute(self, index=0):
        self.go_to_world()
        
        # self.click_ri_chang()
        # self.scroll_and_click(direction='down')

        click_region(self.tzxy_coords_manager.menu_arrow())

        self.get_tzxy_icon_coords(wait_time=3, target_region='挑战仙缘图标', is_to_click=True, click_wait_time=3, to_raise_exception=True)

        # 确认`仙缘页面`是否打开
        self.get_open_tiao_zhan_xian_yuan_coords(wait_time=3, target_region='仙缘页面', is_to_click=False, to_raise_exception=True)
        
        if self.wei_mian == '人界':
            ren_jie_coords = self.get_ren_jie_coords(
                wait_time=3, target_region='人界', is_to_click=True, wait_time_before_click=1, to_raise_exception=False
            )
            if ren_jie_coords is None:
                click_region(self.tzxy_coords_manager.all_xian_yuan())      

        elif self.wei_mian == '灵界':
            self.get_ling_jie_coords(wait_time=3, target_region='灵界', is_to_click=True, wait_time_before_click=1, to_raise_exception=False)

        else:
            raise ValueError(f"未知的位面: {self.wei_mian}!")

        try:
            self.scroll_and_click(
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
        self.get_battle_over_coords(wait_time=60, target_region='战斗结束', is_to_click=True, wait_time_before_click=5)

if __name__ == '__main__':

    resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)

    main_region_coords = get_game_page_coords(resolution = resolution)

    tzxy_coords_manager = TiaoZhanXianYuanCoordsManager(main_region_coords)
    executor = TiaoZhanXianYuanExecutor(tzxy_coords_manager, xian_yuan_role_name='势不两立', wei_mian='灵界')
    executor.execute()
