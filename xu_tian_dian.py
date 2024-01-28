import time
from datetime import datetime
import pyautogui
import numpy as np
from typing import Tuple
from utils_adb import *
from swy_coords_manager import BaseCoordsManager
from swy_event_executor import BaseExecutor
from xiuxian_exception import *

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True
resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)

class XuTianDianCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)

    def main_page(self):
        diff = (362, 1591, 78, 252)
        return self.calculate_relative_coords(diff)

    def main_menus(self):
        diff = (355, 1546, 652, 295)
        return self.calculate_relative_coords(diff)
    
    def task_menus(self):
        diff = (79, 216, 379, 118)
        return self.calculate_relative_coords(diff)
    
    def ling_qu_pos(self):
        diff = (546, 439, 0, 0)
        return self.calculate_relative_coords(diff)
    
    def enable_skip_tan_cha(self):
        diff = (906, 1538, 47, 44)
        return self.calculate_relative_coords(diff)
    
    def tan_chan_and_tiao_zhan(self):
        diff = (212, 1264, 186, 164)
        return self.calculate_relative_coords(diff)

    def exit_2(self):
        diff = (416, 1579, 0, 0)
        return self.calculate_relative_coords(diff)
    
    # def tiao_zhan_region(self):
    #     diff = (27, 64, 321, 62)
    #     return self.calculate_relative_coords(diff)
    
    # def close_alert(self):
    #     diff = (345, 1097, 62, 57)
    #     return self.calculate_relative_coords(diff)

class XuTianDianExecutor(BaseExecutor):
    def __init__(self, xtd_coords_manager: XuTianDianCoordsManager, use_si_bei: bool = False):
        super().__init__(xtd_coords_manager)
        self.xtd_coords_manager = xtd_coords_manager
        # self.server_nums = server_nums
        self.use_si_bei = use_si_bei
        self.event_name = f'虚天殿'
        self.cat_dir = 'xu_tian_dian'

    @wait_region
    def get_xu_tian_dian_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        # return get_region_coords(
        #     f'xu_tian_dian_{self.server_nums}',
        #     main_region_coords=self.main_region_coords,
        #     confidence=0.8,
        #     cat_dir=self.cat_dir ,
        # )
        xu_tian_dian_imgs = [
            {'target_region_image': 'xu_tian_dian_16', 'main_region_coords': self.main_region_coords, 'confidence': 0.8, 'grayscale': False, 'cat_dir': self.cat_dir},
            {'target_region_image': 'xu_tian_dian_2', 'main_region_coords': self.main_region_coords, 'confidence': 0.8, 'grayscale': False, 'cat_dir': self.cat_dir},
        ]

        return get_region_coords_by_multi_imgs(xu_tian_dian_imgs)
    
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
                search_region_coords=self.xtd_coords_manager.task_menus(),
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
            
            click_region(self.xtd_coords_manager.ling_qu_pos())
    

    @wait_region
    def get_main_page_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'main_page',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_qian_wang_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'qian_wang',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_qian_wang_alert_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'qian_wang_alert',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_xu_tian_bao_tu_coords(self, wait_time, target_region, is_to_click, wait_time_before_click, to_raise_exception):
        xu_tian_bao_tu_imgs = [
            {'target_region_image': 'xu_tian_bao_tu1', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': self.cat_dir},
            {'target_region_image': 'xu_tian_bao_tu2', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': self.cat_dir},
        ]

        return get_region_coords_by_multi_imgs(xu_tian_bao_tu_imgs)
    
    @wait_region
    def get_whether_skip_tan_cha_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'whether_skip_tan_cha',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir ,
        )

    @wait_region
    def get_skip_tan_cha_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'skip_tan_cha',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir ,
        )
    
    def check_skip_tan_cha(self):
        
        self.get_xu_tian_bao_tu_coords(wait_time=3, target_region="虚天宝图", is_to_click=True, wait_time_before_click=3, to_raise_exception=True)

        skip_tan_cha_coords = self.get_skip_tan_cha_coords(wait_time=3, target_region="跳过探查", is_to_click=False, to_raise_exception=False)
        
        if skip_tan_cha_coords is None:
            click_region(self.xtd_coords_manager.enable_skip_tan_cha())
        
        click_region(self.xtd_coords_manager.exit())

    @wait_region
    def get_auto_tiao_zhan_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'auto_tiao_zhan',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_open_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'open',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_enable_checkbox_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'enable_checkbox',
            main_region_coords=self.xtd_coords_manager.tan_chan_and_tiao_zhan(),
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
            scroll_seconds=2,
            cat_dir=self.cat_dir,
            in_ri_chang_page=False,
            is_to_click=True,
        )

        start_time = time.time()
        while True:
            if time.time() - start_time > 60:
                print(f"已超过60秒, 退出!")
                break

            self.get_plus_ten_coords(wait_time=1, target_region="加10", is_to_click=True, to_raise_exception=False)
            dui_huan_max_num_coords = self.get_dui_huan_max_num_coords(wait_time=2, target_region="最大购买", is_to_click=False, 
                                                                       to_raise_exception=False)
            
            if dui_huan_max_num_coords is not None:
                print(f"已达到最大兑换数量!")
                break
        
        self.get_dui_huan_coords(wait_time=2, target_region="兑换", is_to_click=True, to_raise_exception=True)

    def execute(self):

        self.go_to_world()

        click_region(self.xtd_coords_manager.ri_cheng())

        self.get_xu_tian_dian_coords(wait_time=20, target_region=self.event_name, is_to_click=True, to_raise_exception=True)

        # 超过60秒, 就退出
        start_time = time.time()
        while True:
            if time.time() - start_time > 60:
                print(f"已超过60秒, 退出!")
                break

            ke_ling_qu_in_shou_yuan_menus_coords = self.get_ke_ling_qu_coords(
                search_region_coords=self.xtd_coords_manager.main_menus(),
                wait_time=3,
                target_region="底部菜单-可领取",
                is_to_click=True,
                to_raise_exception=False,
            )

            if ke_ling_qu_in_shou_yuan_menus_coords is None:
                print(f"已领取完毕!")
                break

            self.ling_qu()
            
        # self.get_main_page_coords(wait_time=3, target_region="主界面", is_to_click=True, to_raise_exception=True)
        click_region(self.xtd_coords_manager.main_page())

        self.get_qian_wang_coords(wait_time=3, target_region="进入活动", is_to_click=True, to_raise_exception=True)

        self.get_qian_wang_alert_coords(wait_time=3, target_region="进入活动提醒", is_to_click=True, to_raise_exception=True)

        while True:
            xu_tian_bao_tu_coords = self.get_xu_tian_bao_tu_coords(wait_time=3, target_region="虚天宝图",  is_to_click=False, wait_time_before_click=3, to_raise_exception=False)
            if xu_tian_bao_tu_coords is not None:
                click_region(xu_tian_bao_tu_coords)
                whether_skip_tan_cha_coords = self.get_whether_skip_tan_cha_coords(wait_time=2, target_region="是否跳过探查", is_to_click=False, to_raise_exception=False)
                if whether_skip_tan_cha_coords is not None:
                    print(f"动画结束, 退出!")
                    click_region(self.xtd_coords_manager.better_exit())
                    break

            click_region(self.xtd_coords_manager.better_exit(), seconds=1)

        self.check_skip_tan_cha()

        self.get_auto_tiao_zhan_coords(wait_time=3, target_region="自动挑战", is_to_click=True, to_raise_exception=False)

        while True:
            open_coords = self.get_open_coords(wait_time=3, target_region="打开", is_to_click=True, to_raise_exception=False)
            if open_coords is None:
                print(f"打开按钮消失, 退出!")
                break
        
        while True:
            enable_checkbox_coords = self.get_enable_checkbox_coords(wait_time=3, target_region="启用", is_to_click=True, to_raise_exception=False)
            if enable_checkbox_coords is None:
                print(f"启用按钮消失, 退出!")
                break
        
        self.get_start_auto_tiao_zhan_coords(wait_time=3, target_region="开始自动挑战", is_to_click=True, to_raise_exception=True)

        self.get_auto_tiao_zhan_over_coords(wait_time=420, target_region="自动挑战结束", is_to_click=True, to_raise_exception=True)

        # 返回世界, 重新进入活动, 然后打开兑换宝阁
        self.go_to_world()

        click_region(self.xtd_coords_manager.ri_cheng())

        self.get_xu_tian_dian_coords(
            wait_time=20,
            target_region=self.event_name,
            is_to_click=True,
            to_raise_exception=True,
        )

        self.dui_huan_cai_liao(target='yao_chi_yu_lian', target_name='瑶池玉莲')

if __name__ == '__main__':

    main_region_coords = get_game_page_coords(resolution = resolution)

    coords_manager = XuTianDianCoordsManager(main_region_coords)
    executor = XuTianDianExecutor(coords_manager, use_si_bei=False)

    executor.execute()
