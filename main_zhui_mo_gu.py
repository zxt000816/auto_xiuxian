import time
import pyautogui
import numpy as np
import pandas as pd
from typing import Tuple
from utils import get_game_page_coords, get_region_coords, click_region, \
                  move_to_specific_coords, scroll_specific_length, extract_int_from_image
from coords_manager import BaseCoordsManager
from event_executor import BaseExecutor, wait_region, click_if_coords_exist, search_region
from xiuxian_exception import *

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True
resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)

def wait_region_not_raise_exception(func):
    def wrapper(self, *args, **kwargs):
        start_time = time.time()
        wait_time = kwargs.get('wait_time', 3)
        target_region = kwargs.get('target_region', None)
        is_to_click = kwargs.get('is_to_click', False)
        print(f"完成: 等待{wait_time}秒, 等待`{target_region}`出现...")
        while True:
            if time.time() - start_time > wait_time:
                return None
            
            result_coords = func(self, *args, **kwargs)
            if result_coords:
                print(f"完成: `{target_region}`出现!")
                if is_to_click:
                    click_region(result_coords)
                    print(f"完成: 点击{target_region}!")
                return result_coords

    return wrapper

try:
    main_region_coords = get_game_page_coords(resolution = resolution)
except Exception as e:
    print(f"未定位到游戏界面!")

class ZhuiMoGuCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)

    def extract_challenge_times(self):
        diff = (449, 1705, 77, 69)
        return self.calculate_relative_coords(diff)
    
    def boss_icon(self):
        diff = (36, 774, 107, 136)
        return self.calculate_relative_coords(diff)
    
    def left_arrow(self):
        diff = (33, 526, 66, 138)
        return self.calculate_relative_coords(diff)
    
    def right_arrow(self):
        diff = (991, 526, 66, 138)
        return self.calculate_relative_coords(diff)
    
    def shou_ling_scroll_start_point(self):
        diff = (540, 960, 0, 0)
        return self.calculate_relative_coords(diff)

class ZhuiMoGuExecutor(BaseExecutor):
    def __init__(self, zmg_coords_manager: ZhuiMoGuCoordsManager, profession_name: str, max_level='炼虚-后期-五层'):
        super().__init__(zmg_coords_manager, 'zhui_mo_gu')
        self.zmg_coords_manager = zmg_coords_manager
        self.profession_name = profession_name
        self.boss_info = pd.read_excel('boss_info.xlsx')
        
        self.max_level_1, self.max_level_2, self.max_level_3 = max_level.split('-')
        self.level_1_numbering = { '练气': 1, '筑基': 2, '结丹': 3, '元婴': 4, '化神': 5, '炼虚': 6 }
        self.level_2_numbering = { '前期': 1, '中期': 2, '后期': 3 }
        self.level_3_numbering = { '一层': 0, '二层': 1, '三层': 2, '四层': 3, '五层': 4, '六层': 5, '七层': 6, '八层': 7, '九层': 8, '十层': 9 }
        self.max_level_numbering = self.level_1_numbering[self.max_level_1] * 100 + self.level_2_numbering[self.max_level_2] * 10 + self.level_3_numbering[self.max_level_3]

        self.profession_boss_info = self.boss_info[(self.boss_info['职业'].str.contains(profession_name)) & (self.boss_info['等级编码'] <= self.max_level_numbering)]

    @wait_region
    def scroll_to_end_indicator_coords(self, wait_time, target_region, is_to_click):
        scroll_end_indicator_coords = get_region_coords(
            'scroll_end_indicator',
            main_region_coords=self.main_region_coords,
            confidence=0.9,
            cat_dir=self.cat_dir,
        )

        move_to_specific_coords(self.zmg_coords_manager.shou_ling_scroll_start_point()[:2], seconds=1)
        scroll_specific_length(-1000, seconds=3)

        return scroll_end_indicator_coords
    
    @wait_region
    def get_qian_wang_tiao_zhan_coords(self, wait_time, target_region, is_to_click):
        qian_wang_tiao_zhan_coords = get_region_coords(
            'qian_wang_tiao_zhan',
            main_region_coords=self.main_region_coords,
            confidence=0.9,
            cat_dir=self.cat_dir,
        )
        return qian_wang_tiao_zhan_coords

    @search_region    
    def search_boss(self, boss, wait_time, target_region, region_to_click, region_to_click_name):
        boss_coords = get_region_coords(
            boss,
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir,
        )
        return boss_coords
    
    @wait_region_not_raise_exception
    def get_shou_ling_leng_que_coords(self, wait_time, target_region, is_to_click):
        shou_ling_leng_que_coords = get_region_coords(
            'shou_ling_leng_que',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir,
        )
        return shou_ling_leng_que_coords
    
    @wait_region_not_raise_exception
    def get_ci_shu_not_enough_coords(self, wait_time, target_region, is_to_click):
        ci_shu_not_enough_coords = get_region_coords(
            'ci_shu_not_enough',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir,
        )
        return ci_shu_not_enough_coords
    
    @wait_region
    def get_shou_ling_icon_coords(self, wait_time, target_region, is_to_click):
        shou_ling_icon_coords = get_region_coords(
            'shou_ling_icon',
            main_region_coords=self.main_region_coords,
            confidence=0.6,
            cat_dir=self.cat_dir,
        )
        return shou_ling_icon_coords

    def go_to_shou_ling_page(self, boss, boss_name, method):
        if method not in ['日常图标', '首领图标']:
            raise ValueError(f"method参数错误, 应为`日常图标`或`首领图标`")
        
        if method == '日常图标':
            self.click_ri_chang()
            self.scoll_and_click(direction='down')
        else:
            # 检查是否有首领图标, 如果有, 点击首领图标, 没有则报错
            self.get_shou_ling_icon_coords(wait_time=120, target_region='首领图标', is_to_click=True)

        # 滚动到首领列表底端, 然后点击最后一个首领打开首领页面     
        self.scroll_to_end_indicator_coords(wait_time=60, target_region='炼虚后期-霜晶云凤', is_to_click=True)
        # 点击左箭头, 直到匹配到当前正在挑战的首领
        self.search_boss(boss, wait_time=60, target_region=boss_name, region_to_click=self.zmg_coords_manager.left_arrow(), region_to_click_name='左箭头')

    def check_boss_state(self, boss, boss_name, method='首领图标'):
        self.go_to_shou_ling_page(boss, boss_name, method)
        # 如果匹配到当前正在挑战的首领, 则停留在当前页面, 直到观察到首领冷却, 代表首领挑战结束
        shou_ling_leng_que_coords = self.get_shou_ling_leng_que_coords(wait_time=360, target_region='首领冷却', is_to_click=False)
        if shou_ling_leng_que_coords is not None:
            print(f"首领被击败, 等待冷却中...")
            return True
        else:
            print(f"首领未被击败, 重新挑战...")
            return False

    def execute(self):
        self.go_to_world()

        try:
            for i, row in self.profession_boss_info.iterrows():
                boss_name = row['首领名称']
                boss = row['英文名']

                self.go_to_shou_ling_page(boss, boss_name, method='日常图标')

                shou_ling_leng_que_coords = self.get_shou_ling_leng_que_coords(wait_time=2, target_region='首领冷却', is_to_click=False)
                if shou_ling_leng_que_coords is not None:
                    print(f"首领冷却中，跳过{boss_name}")
                    self.go_to_world()
                    continue

                self.get_qian_wang_tiao_zhan_coords(wait_time=2, target_region='前往挑战', is_to_click=True)
                ci_shu_not_enough_coords = self.get_ci_shu_not_enough_coords(wait_time=2, target_region='次数不足', is_to_click=False)
                if ci_shu_not_enough_coords is not None:
                    click_region(self.zmg_coords_manager.exit())
                    raise CiShuNotEnoughException(f"次数不足，结束坠魔谷挑战!")
                
                boss_state = self.check_boss_state(boss, boss_name, method='首领图标')
                if boss_state:
                    print(f"首领被击败, 寻找下一个首领...")
                    self.go_to_world()
                    continue
                else:
                    raise BossNotDefeatedException(f"首领未被击败, 重新挑战...")

        except Exception as e:
            print(e)

        self.go_to_world()

coords_manager = ZhuiMoGuCoordsManager(main_region_coords)
executor = ZhuiMoGuExecutor(coords_manager, '法', max_level='化神-前期-十层')

executor.execute()
