import pyautogui
import numpy as np
from typing import Tuple
import time
from utils import *
from coords_manager import BaseCoordsManager
from event_executor import BaseExecutor
from xiuxian_exception import *

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True

class YouliCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)
    
    def youli_start(self): # 游历界面-前往游历按钮:
        diff = (392, 1526, 302, 98)
        return self.calculate_relative_coords(diff)
    
    def youli_end_one_time(self): # 游历界面-游历结束一次
        diff = (414, 1618, 265, 94)
        return self.calculate_relative_coords(diff)
    
    def youli_times_store(self): # 游历次数不足时, 弹出的购买界面
        diff = (107, 318, 858, 1226)
        return self.calculate_relative_coords(diff)

    def buy_button_in_store(self): # 在日常列表界面点击游历, 弹出购买界面时, `购买并使用`按钮的位置
        diff = (376, 1426, 334, 123)
        return self.calculate_relative_coords(diff)
    
    def price_in_store(self): # 在日常列表界面点击游历, 弹出购买界面时, 价格后面的数字的位置
        diff = (574, 1318, 72, 45)
        return self.calculate_relative_coords(diff)
    
    def current_lingshi(self):
        diff = (573, 1372, 166, 50)
        return self.calculate_relative_coords(diff)
    
    def xiu_xian_zhuan(self):
        diff = (910, 123, 50, 85)
        return self.calculate_relative_coords(diff)

class YouLiExecutor(BaseExecutor):
    def __init__(
        self,
        youli_coords_manager: YouliCoordsManager,
        place_name: str='南疆',
        buy_times: int=0,
    ):
        super().__init__(youli_coords_manager, 'youli')
        self.youli_coords_manager = youli_coords_manager
        self.place_name = place_name
        self.buy_times = buy_times
        # self.place_name_dict = {
        #     '镜州': 'jing_zhou',
        #     '冰海': 'bing_hai',
        #     '大晋': 'da_jin',
        #     '南疆': 'nan_jiang',
        #     '地渊冥河': 'di_yuan_ming_he',
        #     '火瑚群岛': 'huo_hu_qun_dao',
        # }
        # self.place = self.place_name_dict[self.place_name]

    @wait_region
    def get_xiu_xian_zhuan_you_li(self, wait_time, target_region, is_to_click, click_wait_time, to_raise_exception):
        return get_region_coords(
            'xiu_xian_zhuan_you_li',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )

    # @wait_region
    # def get_place_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
    #     return get_region_coords(
    #         self.place,
    #         main_region_coords=self.main_region_coords,
    #         confidence=0.8,
    #         cat_dir=self.cat_dir,
    #     )
    
    @wait_region
    def get_place_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        place_imgs = [
            {'target_region_image': 'huo_hu_qun_dao', 'main_region_coords': self.main_region_coords, 'confidence': 0.8, 'cat_dir': self.cat_dir},
            {'target_region_image': 'di_yuan_ming_he', 'main_region_coords': self.main_region_coords, 'confidence': 0.8, 'cat_dir': self.cat_dir},
            {'target_region_image': 'nan_jiang', 'main_region_coords': self.main_region_coords, 'confidence': 0.8, 'cat_dir': self.cat_dir},
            {'target_region_image': 'da_jin', 'main_region_coords': self.main_region_coords, 'confidence': 0.8, 'cat_dir': self.cat_dir},
            {'target_region_image': 'bing_hai', 'main_region_coords': self.main_region_coords, 'confidence': 0.8, 'cat_dir': self.cat_dir},
            {'target_region_image': 'jing_zhou', 'main_region_coords': self.main_region_coords, 'confidence': 0.8, 'cat_dir': self.cat_dir},
        ]
        return get_region_coords_by_multi_imgs(place_imgs)
    
    @wait_region
    def get_buy_icon_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'buy_icon',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_go_to_you_li_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'go_to_you_li',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_confirm_in_you_li_one_time_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'confirm_in_you_li_one_time',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_buy_button_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'buy_button',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir,
        )

    @wait_region
    def get_you_li_over_indicator_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        you_li_over_indicator_imgs = [
            {'target_region_image': 'you_li_over_indicator1', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'cat_dir': self.cat_dir},
            {'target_region_image': 'you_li_over_indicator2', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'cat_dir': self.cat_dir},
        ]
        return get_region_coords_by_multi_imgs(you_li_over_indicator_imgs)

    def execute(self):

        self.go_to_world()

        click_region(self.youli_coords_manager.xiu_xian_zhuan())

        self.get_xiu_xian_zhuan_you_li(wait_time=3, target_region='修仙传_游历', is_to_click=True, click_wait_time=5, to_raise_exception=True)

        self.get_buy_icon_coords(wait_time=2, target_region='购买图标', is_to_click=True, to_raise_exception=True)

        self.buy_times_in_store(self.buy_times, 'buy_times_is_not_enough')
        
        self.get_place_coords(wait_time=5, target_region=self.place_name, is_to_click=True, to_raise_exception=True)

        # 超过30秒就退出
        start_time = time.time()
        while True:
            if time.time() - start_time > 30:
                break
            
            self.get_go_to_you_li_coords(wait_time=3, target_region='前往游历', is_to_click=True, to_raise_exception=True)

            you_li_over_indicator_coords = self.get_you_li_over_indicator_coords(
                wait_time=2, target_region='购买并使用', is_to_click=False, to_raise_exception=False
            )

            if you_li_over_indicator_coords is not None:
                print('游历结束')
                break

            self.get_confirm_in_you_li_one_time_coords(wait_time=3, target_region='游历结束一次', is_to_click=True, to_raise_exception=True)

        for _ in range(3):
            click_region(self.youli_coords_manager.better_exit())

if __name__ == '__main__':

    main_region_coords = get_game_page_coords() # (x, y, width, height)

    coords_manager = YouliCoordsManager(main_region_coords)
    
    youli_executor = YouLiExecutor(
        youli_coords_manager=coords_manager,
        place_name='地渊冥河', # 冰海 or 南疆 or 地渊冥河
        buy_times=0
    )

    youli_executor.execute()
