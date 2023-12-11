import time
import pyautogui
import numpy as np
import pandas as pd
from typing import Tuple
from utils import *
from coords_manager import BaseCoordsManager
from event_executor import BaseExecutor
from xiuxian_exception import *

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True
resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)

try:
    main_region_coords = get_game_page_coords(resolution = resolution)
except Exception as e:
    print(f"未定位到游戏界面!")

def mouse_down_if_coords_exist(func):
    def wrapper(self, *args, **kwargs):
        duration = kwargs.get('duration', 5)
        target_region = kwargs.get('target_region', None)
        coords = func(self, *args, **kwargs)
        x = int(round(coords[0] + coords[2] / 2))
        y = int(round(coords[1] + coords[3] / 2))
        if coords is not None:
            print(f'长按 `{target_region}` 按钮 {duration} 秒')
            pyautogui.mouseDown(x, y, button='left', duration=duration)
                
    return wrapper

class XiuLianCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)

    def xiu_lian_small(self):
        diff = (81, 1584, 252, 277)
        return self.calculate_relative_coords(diff)
    
    def xiu_lian_left_arrow(self):
        diff = (67, 1431, 52, 100)
        return self.calculate_relative_coords(diff)

class XiuLianExecutor(BaseExecutor):
    def __init__(self, xl_coords_manager: XiuLianCoordsManager):
        super().__init__(xl_coords_manager, 'xiu_lian')
        self.xl_coords_manager = xl_coords_manager

    # @click_if_coords_exist
    # def get_xiu_lian_left_arrow_coords(self, target_region, to_raise_exception):
    #     return get_region_coords(
    #         'xiu_lian_left_arrow',
    #         main_region_coords=self.main_region_coords,
    #         confidence=0.8,
    #         cat_dir=self.cat_dir,
    #     )

    @wait_region    
    def get_xiu_lian_icon_coords(self, wait_time, target_region, is_to_click):
        click_region(self.xl_coords_manager.xiu_lian_left_arrow(), seconds=1)
        return get_region_coords(
            'xiu_lian_icon',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )

    @wait_region_not_raise_exception
    def get_fu_yong_over_coords(self, wait_time, target_region, is_to_click):
        return get_region_coords(
            'fu_yong_over',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
    
    @click_if_coords_exist
    def get_ti_sheng_coords(self, target_region):
        return get_region_coords(
            'ti_sheng',
            main_region_coords=self.main_region_coords,
            confidence=0.6,
            cat_dir=self.cat_dir,
        )
    
    @mouse_down_if_coords_exist
    def get_xiu_lian_xin_de_coords(self, duration, target_region):
        return get_region_coords(
            'xiu_lian_xin_de',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
    
    @mouse_down_if_coords_exist
    def get_qian_xiu_xin_de_yi_shi_coords(self, duration, target_region):
        return get_region_coords(
            'qian_xiu_xin_de_yi_shi',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir,
        )

    def execute(self):
        # self.go_to_world()
        # # 进入修炼
        # click_region(self.xl_coords_manager.xiu_lian_small(), seconds=5)
        # # 寻找并点击修炼图标
        # self.get_xiu_lian_icon_coords(wait_time=15, target_region='修炼图标', is_to_click=True)
        # # 检查是否弹出了丹药服用结束的窗口
        # fu_yong_over_coords = self.get_fu_yong_over_coords(wait_time=2, target_region='服用结束', is_to_click=False)
        # if fu_yong_over_coords is not None:
        #     print('完成: 弹出了丹药服用结束的窗口，点击退出!')
        #     click_region(self.xl_coords_manager.exit())
        
        # 点击提升按钮
        self.get_ti_sheng_coords(target_region='提升')

        # 点击修炼心得
        self.get_xiu_lian_xin_de_coords(duration=10, target_region='修炼心得')

        self.get_qian_xiu_xin_de_yi_shi_coords(duration=10, target_region='潜修心得-一时')
        
coords_manager = XiuLianCoordsManager(main_region_coords)
executor = XiuLianExecutor(coords_manager)

executor.execute()


