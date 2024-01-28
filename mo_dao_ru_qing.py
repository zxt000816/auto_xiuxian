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

class MoDaoRuQingCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)

    def mo_dao_ru_qing_menus(self):
        diff = (345, 1562, 663, 284)
        return self.calculate_relative_coords(diff)
    
    def task_menus(self):
        diff = (79, 216, 379, 118)
        return self.calculate_relative_coords(diff)
    
    def ling_qu_pos(self):
        diff = (546, 439, 0, 0)
        return self.calculate_relative_coords(diff)
    
    def tiao_zhan_region(self):
        diff = (27, 64, 321, 62)
        return self.calculate_relative_coords(diff)
    
    def close_alert(self):
        diff = (345, 1097, 62, 57)
        return self.calculate_relative_coords(diff)

class MoDaoRuQingExecutor(BaseExecutor):
    def __init__(self, mdrq_coords_manager: MoDaoRuQingCoordsManager, server_nums: int, use_si_bei: bool = False):
        super().__init__(mdrq_coords_manager)
        self.mdrq_coords_manager = mdrq_coords_manager
        self.server_nums = server_nums
        self.use_si_bei = use_si_bei
        self.event_name = f'魔道入侵[{self.server_nums}]跨'
        self.cat_dir = 'mo_dao_ru_qing'

    @wait_region
    def get_mo_dao_ru_qing_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            f'mo_dao_ru_qing_{self.server_nums}',
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
                search_region_coords=self.mdrq_coords_manager.task_menus(),
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
            
            click_region(self.mdrq_coords_manager.ling_qu_pos())
    

    @wait_region
    def get_main_page_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'main_page',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir ,
        )
    

    @wait_region
    def get_qian_wang_da_di_tu_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'qian_wang_da_di_tu',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_tan_cha_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'tan_cha',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_confirm_tan_cha(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'confirm_tan_cha',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir ,
        )

    @wait_region
    def get_tan_cha_over(self, wait_time, target_region, is_to_click, other_region_coords, to_raise_exception):
        tan_cha_over_imgs = [
            {'target_region_image': 'tan_cha_over1', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': self.cat_dir},
            {'target_region_image': 'tan_cha_over2', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': self.cat_dir},
        ]

        return get_region_coords_by_multi_imgs(tan_cha_over_imgs)

    @wait_region
    def get_tiao_zhan_dui_xiang_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        tiao_zhan_dui_xiang_imgs = [
            {'target_region_image': 'tiao_zhan_dui_xiang1', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': self.cat_dir},
            {'target_region_image': 'tiao_zhan_dui_xiang2', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': self.cat_dir},
        ]

        return get_region_coords_by_multi_imgs(tiao_zhan_dui_xiang_imgs)
    
    @wait_region
    def get_qian_wang_tiao_zhan_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'qian_wang_tiao_zhan',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_close_alert_coords(self, wait_time, target_region, is_to_click, other_region_coords, to_raise_exception):
        return get_region_coords(
            'close_alert',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_dan_ren_tiao_zhan_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'dan_ren_tiao_zhan',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_tiao_zhan_over_coords(self, wait_time, target_region, is_to_click, other_region_coords, wait_time_before_click, to_raise_exception):
        return get_region_coords(
            'tiao_zhan_over',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_tiao_zhan_shi_jian_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'tiao_zhan_shi_jian',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_tiao_zhan_ci_shu_not_enough_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'tiao_zhan_ci_shu_not_enough',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
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

    @wait_region
    def get_confirm_go_to_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'confirm_go_to',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir ,
        )
    
    @wait_region
    def get_skip(self, wait_time, target_region, is_to_click, click_wait_time, to_raise_exception):
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

    def process_others(self):
        self.get_confirm_go_to_coords(wait_time=5, target_region="确认进入", is_to_click=True, to_raise_exception=False)
        self.get_skip(wait_time=4, target_region="跳过", is_to_click=True, click_wait_time=0, to_raise_exception=False)
        self.get_confirm_skip(wait_time=4, target_region="确认跳过", is_to_click=True, to_raise_exception=False)
        time.sleep(10)

    def execute(self):
        self.go_to_world()

        click_region(self.mdrq_coords_manager.ri_cheng())

        self.get_mo_dao_ru_qing_coords(
            wait_time=10,
            target_region=self.event_name,
            is_to_click=True,
            to_raise_exception=True,
        )

        start_time = time.time()
        while True:
            if time.time() - start_time > 60:
                print(f"已超过60秒, 退出!")
                break
            
            qian_wang_da_di_tu_coords = self.get_qian_wang_da_di_tu_coords(wait_time=2, target_region="进入活动", is_to_click=False, to_raise_exception=False)
            if qian_wang_da_di_tu_coords is not None:
                break
            click_region(self.mdrq_coords_manager.exit())

        # 超过60秒, 就退出
        start_time = time.time()
        while True:
            if time.time() - start_time > 60:
                print(f"已超过60秒, 退出!")
                break

            ke_ling_qu_in_shou_yuan_menus_coords = self.get_ke_ling_qu_coords(
                search_region_coords=self.mdrq_coords_manager.mo_dao_ru_qing_menus(),
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

        self.get_qian_wang_da_di_tu_coords(wait_time=2, target_region="进入活动", is_to_click=True, to_raise_exception=True)
        
        self.process_others()

        while True:
            self.get_tan_cha_coords(wait_time=2, target_region="探查", is_to_click=True, to_raise_exception=True)

            tan_cha_over_coords = self.get_tan_cha_over(
                wait_time=2, target_region="探查结束", is_to_click=True, 
                other_region_coords=self.mdrq_coords_manager.exit(), to_raise_exception=False
            )
            if tan_cha_over_coords is not None:
                print(f"探查结束!")
                break

            self.get_confirm_tan_cha(wait_time=5, target_region="确认探查", is_to_click=True, to_raise_exception=True)

        time.sleep(3)

        start_time = time.time()
        while True:
            if time.time() - start_time > 600:
                print(f"已超过600秒, 退出!")
                break

            self.get_tiao_zhan_shi_jian_coords(wait_time=10, target_region="挑战事件", is_to_click=True, to_raise_exception=True)

            tiao_zhan_dui_xiang_coords = self.get_tiao_zhan_dui_xiang_coords(wait_time=2, target_region="挑战对象", is_to_click=True, to_raise_exception=False)
            if tiao_zhan_dui_xiang_coords is None:
                print(f"没有挑战对象, 退出!")
                break

            self.get_qian_wang_tiao_zhan_coords(wait_time=2, target_region="前往挑战", is_to_click=True, to_raise_exception=True)

            tiao_zhan_ci_shu_not_enough_coords = self.get_tiao_zhan_ci_shu_not_enough_coords(wait_time=2, target_region="挑战次数不足", is_to_click=True, to_raise_exception=False)
            if tiao_zhan_ci_shu_not_enough_coords is not None:
                print(f"挑战次数不足, 退出!")
                break

            close_alert_coords = self.get_close_alert_coords(wait_time=2, target_region="关闭弹窗", is_to_click=True, 
                                        other_region_coords=self.mdrq_coords_manager.close_alert(), to_raise_exception=False)

            if close_alert_coords is not None:
                self.get_dan_ren_tiao_zhan_coords(wait_time=2, target_region="单人挑战", is_to_click=True, to_raise_exception=True)
                tiao_zhan_ci_shu_not_enough_coords = self.get_tiao_zhan_ci_shu_not_enough_coords(wait_time=2, target_region="挑战次数不足", is_to_click=True, to_raise_exception=False)
                if tiao_zhan_ci_shu_not_enough_coords is not None:
                    print(f"挑战次数不足, 退出!")
                    break
                
            self.get_tiao_zhan_over_coords(wait_time=120, target_region="挑战结束", is_to_click=True, other_region_coords=self.mdrq_coords_manager.exit(), 
                                           wait_time_before_click=1, to_raise_exception=False)
    

        # 返回世界, 重新进入活动, 然后打开兑换宝阁
        self.go_to_world()

        click_region(self.mdrq_coords_manager.ri_cheng())

        self.get_mo_dao_ru_qing_coords(
            wait_time=10,
            target_region=self.event_name,
            is_to_click=True,
            to_raise_exception=True,
        )

        self.dui_huan_cai_liao(target='yao_chi_yu_lian', target_name='瑶池玉莲')

if __name__ == '__main__':
    main_region_coords = get_game_page_coords(resolution = resolution)

    coords_manager = MoDaoRuQingCoordsManager(main_region_coords)
    executor = MoDaoRuQingExecutor(coords_manager, server_nums=4, use_si_bei=False)

    executor.execute()
