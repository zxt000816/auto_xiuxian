import time
import pyautogui
import numpy as np
from typing import Tuple
from utils_adb import *
from swy_coords_manager import BaseCoordsManager
from swy_event_executor import BaseExecutor
from xiuxian_exception import *

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True

class ShouYuanTanMiCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)

    def shou_yuan_menus(self):
        diff = (351, 1567, 662, 282)
        return self.calculate_relative_coords(diff)
    
    def task_menus(self):
        diff = (83, 219, 564, 102)
        return self.calculate_relative_coords(diff)
    
    def ling_qu_pos(self):
        diff = (546, 439, 0, 0)
        return self.calculate_relative_coords(diff)
    
    def confirm_button_in_alert_for_next_region(self):
        diff = (580, 1223, 308, 100)
        return self.calculate_relative_coords(diff)
    
    def if_only_use_free_times(self):
        diff = (258, 1213, 94, 91)
        return self.calculate_relative_coords(diff)
    
    def do_not_stop(self):
        diff = (262, 1303, 83, 83)
        return self.calculate_relative_coords(diff)
    
    def confirm_button_in_auto_tan_cha_over(self):
        diff = (402, 1227, 302, 96)
        return self.calculate_relative_coords(diff)

class ShouYuanTanMiExecutor(BaseExecutor):
    def __init__(self, sytm_coords_manager: ShouYuanTanMiCoordsManager, server_nums: int, only_use_free_times: bool = True):
        super().__init__(sytm_coords_manager)
        self.sytm_coords_manager = sytm_coords_manager
        self.server_nums = server_nums
        self.only_use_free_times = only_use_free_times
        self.event_name = f'兽渊探秘[{self.server_nums}]跨'
        self.cat_dir = 'shou_yuan_tan_mi'
    
    @wait_region
    def get_shou_yuan_tan_mi_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            f'shou_yuan_tan_mi_{self.server_nums}',
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
                search_region_coords=self.sytm_coords_manager.task_menus(),
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
            
            click_region(self.sytm_coords_manager.ling_qu_pos())
    
    @wait_region
    def get_main_page_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'main_page',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_jin_ru_huo_dong(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'jin_ru_huo_dong',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_zi_dong_tan_cha(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'zi_dong_tan_cha',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir ,
        )
    
    def open_or_close_checkbox(self, operation, target_region):
        if operation not in ['open', 'close']:
            raise InvalidOperation(f"操作`{operation}`不合法!")
        
        check_box_imgs = [
            {'target_region_image': 'check_box1', 'main_region_coords': target_region, 'confidence': 0.9, 'cat_dir': self.cat_dir},
            {'target_region_image': 'check_box2', 'main_region_coords': target_region, 'confidence': 0.9, 'cat_dir': self.cat_dir},
        ]

        check_box_coords = get_region_coords_by_multi_imgs(check_box_imgs)

        if operation == 'open':
            if check_box_coords is None:
                click_region(target_region)
                print(f"完成: 没有被勾选, 勾选checkbox")
            else:
                print(f"完成: 已经被勾选, 不需要再勾选")

        if operation == 'close':
            if check_box_coords is None:
                print(f"完成: checkbox已经被取消勾选!")
            else:
                click_region(target_region)
                print(f"完成: 没有被取消勾选, 取消勾选checkbox!")

    @wait_region
    def get_start_auto_tan_cha(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'start_auto_tan_cha',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_auto_tan_cha_over(self, wait_time, target_region, is_to_click, other_region_coords, to_raise_exception):
        
        auto_tan_cha_over_imgs = [
            {'target_region_image': 'auto_tan_cha_over1', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'cat_dir': self.cat_dir},
            {'target_region_image': 'auto_tan_cha_over2', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'cat_dir': self.cat_dir},
        ]
        return get_region_coords_by_multi_imgs(auto_tan_cha_over_imgs)

    @wait_region
    def get_skip(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'skip',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir ,
        )

    @wait_region
    def get_confirm_skip(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'confirm_skip',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_stop_zi_dong(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'stop_zi_dong',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir ,
        )

    @wait_region
    def get_create_team1(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'create_team1',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_create_team2(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'create_team2',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_create_team3(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'create_team3',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir ,
        )
    
    def create_team(self):
        create_team_coords = self.get_create_team1(wait_time=3, target_region="创建队伍1", is_to_click=True, to_raise_exception=False)
        if create_team_coords is None:
            print(f"已创建队伍!")
            return
        
        self.get_create_team2(wait_time=3, target_region="创建队伍2", is_to_click=True, to_raise_exception=True)
        self.get_create_team3(wait_time=3, target_region="创建队伍3", is_to_click=True, to_raise_exception=True)
        time.sleep(2)
        click_region(self.sytm_coords_manager.exit())

    def process_others(self):
        self.get_skip(wait_time=4, target_region="跳过", is_to_click=True, to_raise_exception=False)
        self.get_confirm_skip(wait_time=4, target_region="确认跳过", is_to_click=True, to_raise_exception=False)

    def execute(self):
        self.go_to_world()

        click_region(self.sytm_coords_manager.ri_cheng())

        self.get_shou_yuan_tan_mi_coords(
            wait_time=3,
            target_region=self.event_name,
            is_to_click=True,
            to_raise_exception=True,
        )

        # 超过60秒, 就退出
        start_time = time.time()
        while True:
            if time.time() - start_time > 60:
                print(f"已超过60秒, 退出!")
                break

            ke_ling_qu_in_shou_yuan_menus_coords = self.get_ke_ling_qu_coords(
                search_region_coords=self.sytm_coords_manager.shou_yuan_menus(),
                wait_time=3,
                target_region="底部菜单-可领取",
                is_to_click=True,
                to_raise_exception=False,
            )

            if ke_ling_qu_in_shou_yuan_menus_coords is None:
                print(f"已领取完毕!")
                break

            self.ling_qu()

        self.get_main_page_coords(wait_time=2, target_region="主界面", is_to_click=True, to_raise_exception=False)

        self.create_team()

        self.get_jin_ru_huo_dong(wait_time=2, target_region="进入活动", is_to_click=True, to_raise_exception=True)

        self.process_others()

        self.get_zi_dong_tan_cha(
            wait_time=10,
            target_region="自动探查",
            is_to_click=True,
            to_raise_exception=True,
        )
        
        operation = 'open' if self.only_use_free_times is False else 'close'
        self.open_or_close_checkbox(operation, self.sytm_coords_manager.if_only_use_free_times())
        self.open_or_close_checkbox('open', self.sytm_coords_manager.do_not_stop())

        self.get_start_auto_tan_cha(wait_time=2, target_region="开始自动探查", is_to_click=True, to_raise_exception=True)
        self.get_stop_zi_dong(wait_time=5, target_region="停止自动探查", is_to_click=False, to_raise_exception=True)
        self.get_auto_tan_cha_over(
            wait_time=1800, target_region="自动探查结束", is_to_click=True,
            other_region_coords=self.sytm_coords_manager.confirm_button_in_auto_tan_cha_over(),
            to_raise_exception=False,
        )

        self.go_to_world()

if __name__ == '__main__':

    resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)

    main_region_coords = get_game_page_coords(resolution = resolution)

    coords_manager = ShouYuanTanMiCoordsManager(main_region_coords)
    executor = ShouYuanTanMiExecutor(coords_manager, server_nums=2, only_use_free_times=True)

    executor.execute()
