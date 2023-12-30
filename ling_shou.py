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



class LingShouCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)

    def region_for_check_mutli_challenge(self):
        diff = (449, 1705, 77, 69)
        return self.calculate_relative_coords(diff)

class LingShouExecutor(BaseExecutor):
    def __init__(self, ls_coords_manager: LingShouCoordsManager, buy_times: int, to_save_times: bool = True):
        super().__init__(ls_coords_manager, 'ling_shou')
        self.ls_coords_manager = ls_coords_manager
        self.buy_times = buy_times
        self.to_save_times = to_save_times
        self.challenge_times = 2

    @wait_region
    def get_open_ling_shou_coords(self, wait_time, target_region, is_to_click):
        open_ling_shou_coords = get_region_coords(
            'open_ling_shou',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir
        )
        return open_ling_shou_coords
    
    @wait_region
    def get_tui_jian_coords(self, wait_time, target_region, is_to_click):
        tui_jian_coords = get_region_coords(
            'tui_jian',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir
        )
        return tui_jian_coords

    def get_multi_challenge_auth_coords(self):
        multi_challenge_auth_coords = get_region_coords(
            'multi_challenge_auth',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir
        )
        return multi_challenge_auth_coords
    
    @click_if_coords_exist
    def get_buy_times_icon_coords(self, target_region):
        buy_times_icon_coords = get_region_coords(
            'buy_times_icon',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir
        )
        return buy_times_icon_coords
    
    @wait_region
    def get_qian_wang_jiao_mie_coords(self, wait_time, target_region, is_to_click):
        qian_wang_jiao_mie_coords = get_region_coords(
            'qian_wang_jiao_mie',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir
        )
        return qian_wang_jiao_mie_coords

    @wait_region
    def get_jiao_mie_over_coords(self, wait_time, target_region, is_to_click):
        jiao_mie_over_coords = get_region_coords(
            'jiao_mie_over',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir
        )
        return jiao_mie_over_coords
    
    @wait_region
    def get_ling_shou_fu_ben_enter_coords(self, wait_time, target_region, is_to_click):
        ling_shou_fu_ben_enter_coords = get_region_coords(
            'ling_shou_fu_ben_enter',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir
        )
        return ling_shou_fu_ben_enter_coords

    def get_buy_times_not_enough_indicator_coords(self):

        buy_times_not_enough_indicator_imgs = [
            {'target_region_image': 'buy_times_not_enough1', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': self.cat_dir},
            {'target_region_image': 'buy_times_not_enough2', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': self.cat_dir},
        ]
        return get_region_coords_by_multi_imgs(buy_times_not_enough_indicator_imgs)

    def execute(self):
        self.go_to_world()
        
        self.click_ri_chang()
        self.scoll_and_click(direction='down')

        self.get_open_ling_shou_coords(wait_time=120, target_region='灵兽界面', is_to_click=False)
        self.get_tui_jian_coords(wait_time=10, target_region='推荐剿灭', is_to_click=True)

        # 如果要存储次数, 那么就要关掉多人挑战, 否则就打开
        multi_challenge_auth_coords = self.get_multi_challenge_auth_coords()
        if self.to_save_times:
            if multi_challenge_auth_coords is not None:
                self.open_or_close_checkbox(
                    operation='close', 
                    target_region=self.ls_coords_manager.region_for_check_mutli_challenge()
                )
            else:
                print("完成: 该账号没有多人挑战的权限!")

        self.get_buy_times_icon_coords(target_region='购买次数图标')
        actual_buy_times = self.buy_times_in_store(self.buy_times, 'buy_times_not_enough1')

        # 如果不存储次数, 那么将购买的次数加到挑战次数上
        if self.to_save_times is False:
            self.challenge_times = self.challenge_times + actual_buy_times

        print(f"完成: 总共挑战次数为{self.challenge_times}次!")
        for i in range(self.challenge_times):
            print(f"完成: 开始第{i + 1}次剿灭!")
            self.get_qian_wang_jiao_mie_coords(wait_time=10, target_region='前往剿灭', is_to_click=True)
            if self.get_buy_times_not_enough_indicator_coords() is not None:
                print("完成: 挑战次数不足!")
                break

            self.get_jiao_mie_over_coords(wait_time=120, target_region='剿灭结束', is_to_click=True)

            if i == self.challenge_times - 1:
                print("完成: 所有次数已用完!")
                break

            self.get_ling_shou_fu_ben_enter_coords(wait_time=120, target_region='灵兽副本进入', is_to_click=True)
            self.get_open_ling_shou_coords(wait_time=120, target_region='灵兽界面', is_to_click=False)
            self.get_tui_jian_coords(wait_time=10, target_region='推荐剿灭', is_to_click=True)

if __name__ == '__main__':

    try:
        main_region_coords = get_game_page_coords(resolution = resolution)
    except Exception as e:
        print(f"未定位到游戏界面!")

    coords_manager = LingShouCoordsManager(main_region_coords)
    executor = LingShouExecutor(coords_manager, buy_times=0, to_save_times=False)
    executor.execute()

