import time
from datetime import datetime
import pyautogui
import numpy as np
from typing import Tuple
from utils import *
from coords_manager import BaseCoordsManager
from event_executor import BaseExecutor
from xiuxian_exception import *

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True


class XianMengZhengBaCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)

    def xian_meng_zheng_ba_menus(self):
        diff = (494, 1552, 514, 306)
        return self.calculate_relative_coords(diff)
    
    def task_menus(self):
        diff = (83, 220, 370, 102)
        return self.calculate_relative_coords(diff)

    def ling_qu_pos(self):
        diff = (546, 439, 0, 0)
        return self.calculate_relative_coords(diff)
    
    def multiple_tiao_zhan_region(self):
        diff = (972, 1465, 100, 86)
        return self.calculate_relative_coords(diff)
    
    def skip_zhan_dou_region(self):
        diff = (982, 1375, 68, 70)
        return self.calculate_relative_coords(diff)

class XianMengZhengBaExecutor(BaseExecutor):
    def __init__(self, xmzb_cm: XianMengZhengBaCoordsManager):
        super().__init__(xmzb_cm)
        self.xmzb_cm = xmzb_cm
        self.event_name = '仙盟争霸'
        self.cat_dir = 'xian_meng_zheng_ba'

    @wait_region
    def get_xian_meng_zheng_ba_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'xian_meng_zheng_ba',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
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
                search_region_coords=self.xmzb_cm.task_menus(),
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
            
            click_region(self.xmzb_cm.ling_qu_pos())
    
    @wait_region
    def get_ke_ling_qu_coords(self, search_region_coords, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'ke_ling_qu',
            main_region_coords=search_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_main_page_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'main_page',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_alert_before_qian_wang_zhan_chang_coords(self, wait_time, target_region, is_to_click, other_region_coords, to_raise_exception):
        return get_region_coords(
            'alert_before_qian_wang_zhan_chang',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir ,
        )

    @wait_region
    def get_qian_wang_zhan_chang_coords(self, wait_time, target_region, is_to_click, wait_time_before_click, to_raise_exception):
        return get_region_coords(
            'qian_wang_zhan_chang',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_meng_ling_coords(self, wait_time, target_region, is_to_click, wait_time_before_click, to_raise_exception):
        meng_ling_imgs = [
            {'target_region_image': 'meng_ling1', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': self.cat_dir},
            {'target_region_image': 'meng_ling2', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': self.cat_dir},
        ]

        return get_region_coords_by_multi_imgs(meng_ling_imgs)
    
    @wait_region
    def get_qian_wang_da_zhen_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'qian_wang_da_zhen',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_gong_ji_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'gong_ji',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_skip_gong_ji_process_coords(self, wait_time, target_region, is_to_click, wait_time_before_click, to_raise_exception):
        return get_region_coords(
            'skip',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_one_time_tiao_zhan_over_coords(self, wait_time, target_region, is_to_click, wait_time_before_click, to_raise_exception):
        return get_region_coords(
            'one_time_tiao_zhan_over',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_confirm_tiao_zhan_over_coords(self, wait_time, target_region, is_to_click, wait_time_before_click, to_raise_exception):
        return get_region_coords(
            'confirm_tiao_zhan_over',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_mian_zhan_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'mian_zhan',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir ,
        )

    def gong_ji(self, gong_ji_coords, multi_tiao_zhan_enabled=False, skip_tiao_zhan_enabled=False):
        
        # mian_zhan_coords = self.get_mian_zhan_coords(wait_time=1, target_region="免战", is_to_click=True, to_raise_exception=False)
        # if mian_zhan_coords is not None:
        #     raise MianZhanException("免战中")

        click_region(gong_ji_coords)

        tiao_zhan_times_not_enough = self.get_tiao_zhan_times_not_enough_coords(
            wait_time=2, target_region="挑战次数不足", is_to_click=False, to_raise_exception=False
        )

        if tiao_zhan_times_not_enough is not None:
            raise TiaoZhanTimesNotEnoughException("挑战次数不足")

        if multi_tiao_zhan_enabled is False:
            if skip_tiao_zhan_enabled is False:
                self.get_skip_gong_ji_process_coords(
                    wait_time=10, target_region="跳过攻击过程", is_to_click=True, wait_time_before_click=1, to_raise_exception=False
                )

            self.get_one_time_tiao_zhan_over_coords(
                wait_time=10, target_region="一次挑战结束", is_to_click=True, wait_time_before_click=1, to_raise_exception=False
            )
        else:
            self.get_confirm_tiao_zhan_over_coords(
                wait_time=10, target_region="确认挑战结束", is_to_click=True, wait_time_before_click=1, to_raise_exception=False
            )

    @wait_region
    def get_multiple_tiao_zhan_enabled_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'multiple_tiao_zhan_enabled',
            main_region_coords=self.xmzb_cm.multiple_tiao_zhan_region(),
            confidence=0.8,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_skip_tiao_zhan_enabled_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'skip_tiao_zhan_enabled',
            main_region_coords=self.xmzb_cm.skip_zhan_dou_region(),
            confidence=0.8,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_tiao_zhan_times_not_enough_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'tiao_zhan_times_not_enough',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_skip_dong_hua_coords(self, wait_time, target_region, is_to_click, wait_time_before_click, to_raise_exception):
        return get_region_coords(
            'skip_dong_hua',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir ,
        )


    def execute(self):

        # self.go_to_world()

        # click_region(self.xmzb_cm.ri_cheng())

        # self.get_xian_meng_zheng_ba_coords(
        #     wait_time=3,
        #     target_region=self.event_name,
        #     is_to_click=True,
        #     to_raise_exception=True,
        # )

        # self.get_alert_before_qian_wang_zhan_chang_coords(wait_time=2, target_region="消息提醒", is_to_click=True, other_region_coords=self.xmzb_cm.exit(), to_raise_exception=False)

        # # 超过60秒, 就退出
        # start_time = time.time()
        # while True:
        #     if time.time() - start_time > 60:
        #         print(f"已超过60秒, 退出!")
        #         break

        #     ke_ling_qu_coords = self.get_ke_ling_qu_coords(
        #         search_region_coords=self.xmzb_cm.xian_meng_zheng_ba_menus(),
        #         wait_time=3,
        #         target_region="底部菜单-可领取",
        #         is_to_click=True,
        #         to_raise_exception=False,
        #     )

        #     if ke_ling_qu_coords is None:
        #         print(f"已领取完毕!")
        #         break

        #     self.ling_qu()

        # self.get_main_page_coords(wait_time=2, target_region="主界面", is_to_click=True, to_raise_exception=False)

        # self.get_qian_wang_zhan_chang_coords(wait_time=2, target_region="前往战场", is_to_click=True, wait_time_before_click=1, to_raise_exception=True)

        # self.get_skip_dong_hua_coords(wait_time=10, target_region="跳过动画", is_to_click=True, wait_time_before_click=2, to_raise_exception=False)

        # time.sleep(10)

        # self.get_meng_ling_coords(wait_time=30, target_region="盟令", is_to_click=True, wait_time_before_click=2, to_raise_exception=True)

        # self.get_qian_wang_da_zhen_coords(wait_time=2, target_region="前往大阵", is_to_click=True, to_raise_exception=True)

        gong_ji_coords = self.get_gong_ji_coords(wait_time=10, target_region="攻击", is_to_click=False, to_raise_exception=True)

        multiple_tiao_zhan_enabled_coords = self.get_multiple_tiao_zhan_enabled_coords(
            wait_time=2, target_region="多次挑战-可用", is_to_click=False, to_raise_exception=False
        )
        multiple_tiao_zhan_enabled = False if multiple_tiao_zhan_enabled_coords is None else True

        skip_tiao_zhan_enabled_coords = self.get_skip_tiao_zhan_enabled_coords(
            wait_time=2, target_region="跳过战斗-可用", is_to_click=False, to_raise_exception=False
        )
        skip_tiao_zhan_enabled = False if skip_tiao_zhan_enabled_coords is None else True
        
        cnt = 0
        while True:
            if cnt % 10 == 0 and multiple_tiao_zhan_enabled is False:
                click_region(self.xmzb_cm.multiple_tiao_zhan_region())
                pyautogui.moveTo(self.xmzb_cm.exit()[:2])

                multiple_tiao_zhan_enabled_coords = self.get_multiple_tiao_zhan_enabled_coords(
                    wait_time=2, target_region="多次挑战-可用", is_to_click=False, to_raise_exception=False
                )
                multiple_tiao_zhan_enabled = False if multiple_tiao_zhan_enabled_coords is None else True

            if cnt % 3 == 0 and skip_tiao_zhan_enabled is False:
                click_region(self.xmzb_cm.skip_zhan_dou_region())
                pyautogui.moveTo(self.xmzb_cm.exit()[:2])

                skip_tiao_zhan_enabled_coords = self.get_skip_tiao_zhan_enabled_coords(
                    wait_time=2, target_region="跳过战斗-可用", is_to_click=False, to_raise_exception=False
                )
                skip_tiao_zhan_enabled = False if skip_tiao_zhan_enabled_coords is None else True

            self.gong_ji(gong_ji_coords, multiple_tiao_zhan_enabled, skip_tiao_zhan_enabled)

            cnt += 1

if __name__ == '__main__':
    resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)

    main_region_coords = get_game_page_coords(resolution = resolution)

    coords_manager = XianMengZhengBaCoordsManager(main_region_coords)
    executor = XianMengZhengBaExecutor(coords_manager)
    
    executor.execute()
