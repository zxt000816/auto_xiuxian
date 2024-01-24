import time
import pyautogui
import numpy as np
import pandas as pd
from typing import Tuple
from utils_adb import *
from coords_manager import BaseCoordsManager
from event_executor import BaseExecutor
from xiuxian_exception import *

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True

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
    
    def switch_coords(self):
        diff = (203, 83, 65, 54)
        return self.calculate_relative_coords(diff)

class ZhuiMoGuExecutor(BaseExecutor):
    def __init__(self, zmg_coords_manager: ZhuiMoGuCoordsManager, profession_name: str, max_level: str, wei_mian: str='人界'):
        super().__init__(zmg_coords_manager, 'zhui_mo_gu')
        self.zmg_coords_manager = zmg_coords_manager
        self.profession_name = profession_name
        self.wei_mian = wei_mian
        self.boss_info: pd.DataFrame = pd.read_excel('boss_info.xlsx', sheet_name=self.wei_mian)
        
        self.max_level_1, self.max_level_2, self.max_level_3 = max_level.split('-')
        self.level_1_numbering = { '练气': 1, '筑基': 2, '结丹': 3, '元婴': 4, '化神': 5, '炼虚': 6 }
        self.level_2_numbering = { '前期': 1, '中期': 2, '后期': 3 }
        self.level_3_numbering = { '一层': 0, '二层': 1, '三层': 2, '四层': 3, '五层': 4, '六层': 5, '七层': 6, '八层': 7, '九层': 8, '十层': 9 }
        self.max_level_numbering = self.level_1_numbering[self.max_level_1] * 100 + self.level_2_numbering[self.max_level_2] * 10 + self.level_3_numbering[self.max_level_3]

        self.profession_boss_info: pd.DataFrame = self.boss_info[(self.boss_info['职业'].str.contains(profession_name)) & (self.boss_info['等级编码'] <= self.max_level_numbering)]

    @wait_region
    def scroll_to_end_indicator_coords(self, wait_time, target_region, is_to_click):
        scroll_end_indicator_coords = get_region_coords(
            'scroll_end_indicator',
            main_region_coords=self.main_region_coords,
            confidence=0.9,
            cat_dir=self.cat_dir,
        )

        # move_to_specific_coords(self.zmg_coords_manager.shou_ling_scroll_start_point()[:2], seconds=1)
        # scroll_length = self.calculate_scroll_length(-1000)
        # scroll_specific_length(-1000 * self.coords_manager.y_ratio, seconds=3)
        # scroll_specific_length(scroll_length, seconds=3)
        scroll_specific_length(
            start_x=0.5,
            end_x=0.5,
            start_y=0.66,
            end_y=0.33,
            seconds=3,
        )

        return scroll_end_indicator_coords
    
    @wait_region
    def scroll_to_any_available_coords(self, wait_time, target_region, is_to_click):
        if self.wei_mian == '人界':
            any_available_imgs = [
                {'target_region_image': 'indicator1', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': 'zhui_mo_gu'},
                {'target_region_image': 'indicator2', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': 'zhui_mo_gu'},
                {'target_region_image': 'indicator3', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': 'zhui_mo_gu'},
                {'target_region_image': 'indicator4', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': 'zhui_mo_gu'},
                {'target_region_image': 'indicator5', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': 'zhui_mo_gu'},
                {'target_region_image': 'indicator6', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': 'zhui_mo_gu'},
                {'target_region_image': 'indicator7', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': 'zhui_mo_gu'},
                {'target_region_image': 'indicator8', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': 'zhui_mo_gu'},
            ]
        elif self.wei_mian == '灵界':
            any_available_imgs = [
                {'target_region_image': 'ling_jie_indicator1', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': 'zhui_mo_gu'},
                {'target_region_image': 'ling_jie_indicator2', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': 'zhui_mo_gu'},
                {'target_region_image': 'ling_jie_indicator3', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': 'zhui_mo_gu'},
            ]

        any_available_coords = get_region_coords_by_multi_imgs(any_available_imgs)
        # scroll_length = self.calculate_scroll_length(500)
        if any_available_coords is None:
            # move_to_specific_coords(self.zmg_coords_manager.shou_ling_scroll_start_point()[:2], seconds=1)
            # scroll_specific_length(scroll_length, seconds=3)
            scroll_specific_length(
                start_x=0.5,
                end_x=0.5,
                start_y=0.66,
                end_y=0.33,
                seconds=3,
            )
        
        return any_available_coords
    
    def determine_order_of_current_boss(self):
        # 进入副本页面和, 根据首领名称, 确定当前首领的顺序
        for i, row in self.boss_info.iterrows():
            _boss = row['英文名']
            _boss_coords = get_region_coords(
                _boss,
                main_region_coords=self.main_region_coords,
                confidence=0.7,
                cat_dir=self.cat_dir,
            )
            if _boss_coords is not None:
                print(f"当前首领为: {row['首领名称']}")
                return row['等级编码']
            
        raise Exception('没有检测到当前首领是哪个!')
    
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
    def get_shou_ling_page_indicator_coords(self, wait_time, target_region, to_raise_exception):
        shou_ling_icon_imgs = [
                {'target_region_image': 'shou_ling_page_indicator1', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': self.cat_dir},
                {'target_region_image': 'shou_ling_page_indicator3', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': self.cat_dir},
                {'target_region_image': 'shou_ling_page_indicator2', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': self.cat_dir},
            ]
        return get_region_coords_by_multi_imgs(shou_ling_icon_imgs)

    @wait_region
    def get_shou_ling_icon_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        shou_ling_icon_imgs = [
            {'target_region_image': 'shou_ling_icon1', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': self.cat_dir},
            {'target_region_image': 'shou_ling_icon2', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': self.cat_dir},
        ]
        return get_region_coords_by_multi_imgs(shou_ling_icon_imgs)
    
    @wait_region
    def get_ling_jie_page_indicator_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        ling_jie_page_indicator_coords = get_region_coords(
            'ling_jie_page_indicator',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir,
        )
        return ling_jie_page_indicator_coords

    def switch_between_ren_jie_and_ling_jie(self):
        if self.wei_mian == '灵界':
            ling_jie_page_indicator_coords = self.get_ling_jie_page_indicator_coords(wait_time=3, target_region='灵界页面_标识', is_to_click=False, to_raise_exception=False)
            if ling_jie_page_indicator_coords is None:
                click_region(self.zmg_coords_manager.switch_coords())

        elif self.wei_mian == '人界':
            ling_jie_page_indicator_coords = self.get_ling_jie_page_indicator_coords(wait_time=3, target_region='灵界页面_标识', is_to_click=False, to_raise_exception=False)
            if ling_jie_page_indicator_coords is not None:
                click_region(self.zmg_coords_manager.switch_coords())

        else:
            raise ValueError(f"未知的位面: {self.wei_mian}")

    def go_to_shou_ling_page(self, boss, boss_name, method):
        if method not in ['日常图标', '首领图标']:
            raise ValueError(f"method参数错误, 应为`日常图标`或`首领图标`")
        
        if method == '日常图标':
            self.click_ri_chang()
            self.scroll_and_click_by_multiple_imgs(
                direction='down',
                targets_imgs_info=[
                    {'target_region_image': 'zhui_mo_gu', 'main_region_coords': self.main_region_coords, 'confidence': 0.8, 'grayscale': False, 'cat_dir': self.cat_dir},
                    {'target_region_image': 'zhui_mo_gu_ling_jie', 'main_region_coords': self.main_region_coords, 'confidence': 0.8, 'grayscale': False, 'cat_dir': self.cat_dir},
                ],
                target_name='坠魔谷/积麟秘境',
            )
        else:
            # 检查是否有首领图标, 如果有, 点击首领图标, 没有则报错
            # 等待120秒
            start_time = time.time()
            while True:
                if time.time() - start_time > 120:
                    raise Exception('没有检测到首领图标!')

                shou_ling_page_indicator_coords = self.get_shou_ling_page_indicator_coords(
                    wait_time=2, 
                    target_region='首领页面_标识', 
                    to_raise_exception=False
                )
                if shou_ling_page_indicator_coords is not None:
                    break

                self.get_shou_ling_icon_coords(wait_time=2, target_region='首领图标', is_to_click=True, to_raise_exception=False)

        # 在首领页面, 切换到灵界或人界
        self.switch_between_ren_jie_and_ling_jie()

        # 滚动到首领列表底端, 然后点击最后一个首领打开首领页面     
        self.scroll_to_any_available_coords(wait_time=60, target_region='任何可以进入副本的区域', is_to_click=True)

        # 判断当前是哪个首领, 获取该首领的等级编码
        current_boss_order = self.determine_order_of_current_boss()
        print(f"当前首领的等级编码为: {current_boss_order}")
        
        # 获取目标首领的等级编码,根据等级编码, 确定点击左箭头还是右箭头
        target_boss_order = self.boss_info[self.boss_info['英文名'] == boss]['等级编码'].item()
        print(f"目标首领的等级编码为: {target_boss_order}")

        if target_boss_order == current_boss_order:
            print(f"当前首领为目标首领, 不需要切换首领!")
            return
        elif target_boss_order > current_boss_order:
            to_click_region = self.zmg_coords_manager.right_arrow()
        else:
            to_click_region = self.zmg_coords_manager.left_arrow()

        self.search_boss(boss, wait_time=60, target_region=boss_name, region_to_click=to_click_region, region_to_click_name='左箭头')

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
                print(f"次数不足，结束坠魔谷挑战!")
                return
            
            self.check_boss_state(boss, boss_name, method='首领图标')
            self.go_to_world()

if __name__ == '__main__':

    resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)
    
    main_region_coords = get_game_page_coords(resolution = resolution)

    coords_manager = ZhuiMoGuCoordsManager(main_region_coords)

    executor = ZhuiMoGuExecutor(coords_manager, '法', max_level='炼虚-中期-十层', wei_mian='人界')

    executor.execute()
