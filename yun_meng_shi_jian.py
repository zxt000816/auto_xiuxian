import time
from datetime import datetime
import pyautogui
import numpy as np
from typing import Tuple
from utils import *
from swy_coords_manager import BaseCoordsManager
from swy_event_executor import BaseExecutor
from xiuxian_exception import *

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True
resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)

class YunMengShiJianCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)

    def main_page(self):
        diff = (359, 1586, 80, 245)
        return self.calculate_relative_coords(diff)

    def main_menus(self):
        diff = (355, 1546, 652, 295)
        return self.calculate_relative_coords(diff)
    
    def task_menus(self):
        diff = (73, 197, 586, 123)
        return self.calculate_relative_coords(diff)
    
    def ling_qu_pos(self):
        diff = (546, 439, 0, 0)
        return self.calculate_relative_coords(diff)
    
    def ymsj_si_bei(self):
        diff = (100, 1028, 661, 93)
        return self.calculate_relative_coords(diff)
    
    def ymsj_ti_li(self):
        diff = (166, 1262, 744, 80)
        return self.calculate_relative_coords(diff)

class YunMengShiJianExecutor(BaseExecutor):
    def __init__(self, ymsj_coords_manager: YunMengShiJianCoordsManager, server_nums: int, use_si_bei: bool = False, use_ti_li: bool = False):
        super().__init__(ymsj_coords_manager)
        self.ymsj_coords_manager = ymsj_coords_manager
        self.server_nums = server_nums
        self.use_si_bei = use_si_bei
        self.use_ti_li = use_ti_li
        self.event_name = f'云梦试剑[{self.server_nums}]跨'
        self.cat_dir = 'yun_meng_shi_jian'

    @wait_region
    def get_yun_meng_shi_jian_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            f'yun_meng_shi_jian_{self.server_nums}',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_ke_ling_qu_coords(self, search_region_coords, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'ke_ling_qu',
            main_region_coords=search_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir ,
        )
    
    # 一直领取, 直到`可领取`的标识消失
    def ling_qu(self):
        is_to_click = True
        # 超过30秒, 就退出
        start_time = time.time()
        while True:
            if time.time() - start_time > 30:
                print(f"已超过20秒, 退出!")
                break
            
            ke_ling_qu_coords = self.get_ke_ling_qu_coords(
                search_region_coords=self.ymsj_coords_manager.task_menus(),
                wait_time=2,
                target_region="任务菜单-可领取",
                is_to_click=is_to_click,
                to_raise_exception=False,
            )

            # 点击一次后, 就不再点击
            is_to_click = False

            if ke_ling_qu_coords is None:
                print(f"已领取完毕!")
                break
            
            click_region(self.ymsj_coords_manager.ling_qu_pos())
    

    @wait_region
    def get_main_page_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'main_page',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir ,
        )

    @wait_region
    def get_auto_tiao_zhan_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'auto_tiao_zhan',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_disable_si_bei_checkbox_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'disable_checkbox',
            main_region_coords=self.ymsj_coords_manager.ymsj_si_bei(),
            confidence=0.8,
            cat_dir=self.cat_dir
        )
    
    @wait_region
    def get_disable_ti_li_checkbox_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'disable_checkbox',
            main_region_coords=self.ymsj_coords_manager.ymsj_ti_li(),
            confidence=0.8,
            cat_dir=self.cat_dir
        )
    
    @wait_region
    def get_enable_si_bei_checkbox_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'enable_checkbox',
            main_region_coords=self.ymsj_coords_manager.ymsj_si_bei(),
            confidence=0.8,
            cat_dir=self.cat_dir
        )
    
    @wait_region
    def get_enable_ti_li_checkbox_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'enable_checkbox',
            main_region_coords=self.ymsj_coords_manager.ymsj_ti_li(),
            confidence=0.8,
            cat_dir=self.cat_dir
        )

    @wait_region
    def get_start_auto_tiao_zhan_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'start_auto_tiao_zhan',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_auto_tiao_zhan_over_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'auto_tiao_zhan_over',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_dui_huan_bao_ge_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'dui_huan_bao_ge',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_plus_ten_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'plus_ten',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_dui_huan_max_num_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'dui_huan_max_num',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_dui_huan_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'dui_huan',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir ,
        )
    
    def dui_huan_cai_liao(self, target='yao_chi_yu_lian', target_name='瑶池玉莲'):
        self.get_dui_huan_bao_ge_coords(wait_time=2, target_region="兑换宝阁", is_to_click=True, to_raise_exception=False)

        self.scroll_and_click(
            direction='down',
            other_target=target,
            other_target_name=target_name,
            confidence=0.7,
            num_of_scroll=5,
            scroll_length=300,
            scroll_seconds=3,
            cat_dir=self.cat_dir,
            in_ri_chang_page=False,
            is_to_click=True,
        )

        start_time = time.time()
        while True:
            if time.time() - start_time > 60:
                print(f"已超过60秒, 退出!")
                break

            self.get_plus_ten_coords(wait_time=1, target_region="加10", is_to_click=True, to_raise_exception=True)
            dui_huan_max_num_coords = self.get_dui_huan_max_num_coords(wait_time=2, target_region="最大购买", is_to_click=False, 
                                                                       to_raise_exception=False)
            
            if dui_huan_max_num_coords is not None:
                print(f"已达到最大兑换数量!")
                break
        
        self.get_dui_huan_coords(wait_time=2, target_region="兑换", is_to_click=True, to_raise_exception=True)

    def execute(self):

        self.go_to_world()

        click_region(self.ymsj_coords_manager.ri_cheng())

        self.get_yun_meng_shi_jian_coords(wait_time=20, target_region=self.event_name, is_to_click=True, to_raise_exception=True)

        # 超过60秒, 就退出
        start_time = time.time()
        while True:
            if time.time() - start_time > 60:
                print(f"已超过60秒, 退出!")
                break

            ke_ling_qu_in_shou_yuan_menus_coords = self.get_ke_ling_qu_coords(
                search_region_coords=self.ymsj_coords_manager.main_menus(),
                wait_time=3,
                target_region="底部菜单-可领取",
                is_to_click=True,
                to_raise_exception=False,
            )

            if ke_ling_qu_in_shou_yuan_menus_coords is None:
                print(f"已领取完毕!")
                break

            self.ling_qu()
            
        click_region(self.ymsj_coords_manager.main_page())

        self.get_auto_tiao_zhan_coords(wait_time=3, target_region="自动挑战", is_to_click=True, to_raise_exception=True)

        if self.use_si_bei:
            self.get_disable_si_bei_checkbox_coords(wait_time=3, target_region="使用四倍关闭", is_to_click=True, to_raise_exception=False)
        else:
            self.get_enable_si_bei_checkbox_coords(wait_time=3, target_region="使用四倍开启", is_to_click=True, to_raise_exception=False)    


        if self.use_ti_li:
            self.get_disable_ti_li_checkbox_coords(wait_time=3, target_region="使用体力关闭", is_to_click=True, to_raise_exception=False)
        else:
            self.get_enable_ti_li_checkbox_coords(wait_time=3, target_region="使用体力开启", is_to_click=True, to_raise_exception=False)
        
        self.get_start_auto_tiao_zhan_coords(wait_time=3, target_region="开始自动挑战", is_to_click=True, to_raise_exception=True)

        self.get_auto_tiao_zhan_over_coords(wait_time=480, target_region="自动挑战结束", is_to_click=True, to_raise_exception=True)

        # 返回世界, 重新进入活动, 然后打开兑换宝阁
        self.go_to_world()

        click_region(self.ymsj_coords_manager.ri_cheng())

        self.get_yun_meng_shi_jian_coords(wait_time=20, target_region=self.event_name, is_to_click=True, to_raise_exception=True)

        self.dui_huan_cai_liao(target='yao_chi_yu_lian', target_name='瑶池玉莲')

if __name__ == '__main__':

    main_region_coords = get_game_page_coords(resolution = resolution)

    coords_manager = YunMengShiJianCoordsManager(main_region_coords)
    executor = YunMengShiJianExecutor(coords_manager, server_nums=2, use_si_bei=True, use_ti_li=True)

    executor.execute()
