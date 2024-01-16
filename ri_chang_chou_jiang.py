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


class RiChangChouJiangCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)

    def lmtb_check_ling_qu(self):
        diff = (472, 1529, 547, 312)
        return self.calculate_relative_coords(diff)
    
    def lmtb_ling_qu(self):
        diff = (99, 203, 939, 180)
        return self.calculate_relative_coords(diff)
    
    def lmtb(self):
        diff = (345, 1560, 133, 276)
        return self.calculate_relative_coords(diff)
    
    def lmtb_yi_zhen(self):
        diff = (931, 1134, 147, 149)
        return self.calculate_relative_coords(diff)
    
    def avoid_hide_next(self):
        diff = (516, 1449, 0, 0)
        return self.calculate_relative_coords(diff)

class RiChangChouJiangExecutor(BaseExecutor):
    def __init__(self, rccj_coords_manager: RiChangChouJiangCoordsManager, chou_jiang_event: str):
        super().__init__(rccj_coords_manager)
        self.rccj_coords_manager = rccj_coords_manager
        self.chou_jiang_event = chou_jiang_event
        self.cat_dir = 'ri_chang_chou_jiang'

    @wait_region
    def get_ri_change_chou_jiang_region(self, wait_time, target_region, is_to_click, click_wait_time, to_raise_exception):
        if self.chou_jiang_event == '灵缈探宝':
            target = 'ling_miao_tan_bao'
        else:
            raise Exception(f'Unknown chou jiang event: {self.chou_jiang_event}')
        
        return get_region_coords(
            target,
            self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir
        )
    
    @wait_region
    def get_task_ling_qu_icon_coords(self, wait_time, target_region, is_to_click, click_wait_time, to_raise_exception):
        return get_region_coords(
            'ling_qu_icon',
            self.rccj_coords_manager.lmtb_check_ling_qu(),
            confidence=0.7,
            cat_dir=self.cat_dir
        )
    
    def ling_qu_task_award(self):
        ling_qu_icon_coords = self.get_task_ling_qu_icon_coords(wait_time=3, target_region="领取图标", 
                                                           is_to_click=True, click_wait_time=2, to_raise_exception=False)

        start_time = datetime.now()
        while True:
            if (datetime.now() - start_time).seconds > 60:
                raise TimeOutException('领取任务奖励超时!')
            
            ling_qu_icon_coords = self.get_task_ling_qu_icon_coords(wait_time=2, target_region='领取图标', 
                                                               is_to_click=False, click_wait_time=0, to_raise_exception=False)
            if ling_qu_icon_coords is None:
                print("领取完成!")
                break

            click_region(self.rccj_coords_manager.lmtb_ling_qu(), seconds=1)

    @wait_region
    def get_ling_shi_icon_coords(self, wait_time, target_region, is_to_click, click_wait_time, to_raise_exception):
        return get_region_coords(
            'ling_qu_icon',
            self.rccj_coords_manager.lmtb(),
            confidence=0.7,
            cat_dir=self.cat_dir
        )
    
    @wait_region
    def get_ling_qu_in_yi_zhen_coords(self, wait_time, target_region, is_to_click, click_wait_time, to_raise_exception):
        return get_region_coords(
            'ling_qu_icon',
            self.rccj_coords_manager.lmtb_yi_zhen(),
            confidence=0.7,
            cat_dir=self.cat_dir
        )

    @wait_region
    def get_dian_ji_kai_qi_coords(self, wait_time, target_region, is_to_click, click_wait_time, to_raise_exception):
        return get_region_coords(
            'dian_ji_kai_qi',
            self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir
        )
    
    @wait_region
    def get_lmtb_qi_zhen_next_coords(self, wait_time, target_region, is_to_click, click_wait_time, to_raise_exception):
        return get_region_coords(
            'lmtb_qi_zhen_next',
            self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir
        )

    def ling_qu_ling_shi(self):
        self.get_ling_shi_icon_coords(wait_time=5, target_region="领取图标", 
                                      is_to_click=True, click_wait_time=1, to_raise_exception=True)
        
        self.get_ling_qu_in_yi_zhen_coords(wait_time=5, target_region="领取灵石", 
                                           is_to_click=True, click_wait_time=3, to_raise_exception=True)
        
        start_time = datetime.now()
        while True:
            if (datetime.now() - start_time).seconds > 120:
                raise TimeOutException('领取灵石超时!')

            self.get_dian_ji_kai_qi_coords(wait_time=5, target_region="点击开启", is_to_click=True, 
                                           click_wait_time=3, to_raise_exception=False)

            lmtb_qi_zhen_next_coords = self.get_lmtb_qi_zhen_next_coords(wait_time=5, target_region="切换下一个", is_to_click=True, 
                                                                         click_wait_time=1, to_raise_exception=False)
            
            pyautogui.moveTo(self.rccj_coords_manager.avoid_hide_next()[:2])
            if lmtb_qi_zhen_next_coords is None:
                print("领取灵石完成!")
                break
    
    @wait_region
    def get_lmtb_main_coords(self, wait_time, target_region, is_to_click, click_wait_time, to_raise_exception):
        lmtb_main_imgs = [
            {'target_region_image': 'lmtb_main1', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': self.cat_dir},
            {'target_region_image': 'lmtb_main2', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': self.cat_dir},
        ]

        return get_region_coords_by_multi_imgs(lmtb_main_imgs)

    @wait_region
    def get_chou_jiang_coords(self, wait_time, target_region, is_to_click, click_wait_time, to_raise_exception):
        if self.chou_jiang_event == '灵缈探宝':
            target = 'lmtb_chou_jiang'
        else:
            raise Exception(f'Unknown chou jiang event: {self.chou_jiang_event}')
        
        return get_region_coords(
            target,
            self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir
        )
    
    @wait_region
    def get_chou_jiang_one_epoch_over_coords(self, wait_time, target_region, is_to_click, click_wait_time, wait_time_before_click, to_raise_exception):
        return get_region_coords(
            'chou_jiang_one_epoch_over',
            self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir
        )
    
    @wait_region
    def get_lmtb_chou_jiang_over_coords(self, wait_time, target_region, is_to_click, click_wait_time, wait_time_before_click, to_raise_exception):
        return get_region_coords(
            'lmtb_chou_jiang_over',
            self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir
        )
    
    def lmtb_chou_jiang(self):
        
        self.get_lmtb_main_coords(wait_time=3, target_region="灵缈探宝主界面", is_to_click=True, 
                                click_wait_time=1, to_raise_exception=True)

        start_time = datetime.now()
        while True:
            if (datetime.now() - start_time).seconds > 60:
                raise TimeOutException('灵缈探宝, 抽奖超时!')
            
            self.get_chou_jiang_coords(
                wait_time=6, target_region="灵缈探宝抽奖", is_to_click=True,
                click_wait_time=1, to_raise_exception=True
            )
            
            lmtb_chou_jiang_over_coords = self.get_lmtb_chou_jiang_over_coords(
                wait_time=3, target_region="灵缈探宝结束", is_to_click=False,
                click_wait_time=1, wait_time_before_click=2, to_raise_exception=False
            )
            if lmtb_chou_jiang_over_coords is not None:
                print("灵缈探宝-抽奖次数不足!")
                click_region(self.rccj_coords_manager.exit())
                break

            self.get_chou_jiang_one_epoch_over_coords(
                wait_time=8, target_region="灵缈探宝一轮结束", is_to_click=True,
                click_wait_time=1, wait_time_before_click=2, to_raise_exception=True
            )

    def execute(self):
        self.go_to_world()

        self.get_ri_change_chou_jiang_region(wait_time=3, target_region=self.chou_jiang_event, is_to_click=True, 
                                             click_wait_time=2, to_raise_exception=True)
        
        self.ling_qu_task_award()

        if self.chou_jiang_event == '灵缈探宝':
            self.lmtb_chou_jiang()

        self.ling_qu_ling_shi()

if __name__ == '__main__':
    resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)

    main_region_coords = get_game_page_coords(resolution = resolution)

    coords_manager = RiChangChouJiangCoordsManager(main_region_coords)
    executor = RiChangChouJiangExecutor(coords_manager, chou_jiang_event='灵缈探宝')

    executor.execute()

