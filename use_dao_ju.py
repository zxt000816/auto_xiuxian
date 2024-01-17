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

class UseDaoJuCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)
    
    def expand_menu(self):
        diff = (968, 1733, 93, 71)
        return self.calculate_relative_coords(diff)
    
    # def use_dao_ju_check_region(self):
    #     diff = (239, 948, 544, 532)
    #     return self.calculate_relative_coords(diff)

    def profession_gong_fa_region(self):
        diff = (80, 285, 775, 116)
        return self.calculate_relative_coords(diff)
    
    def san_huang_ling_wei(self):
        diff = (83, 457, 80, 87)
        return self.calculate_relative_coords(diff)
    
    def shang_pin_gong_fa(self):
        diff = (209, 509, 80, 309)
        return self.calculate_relative_coords(diff)
    
    def zhen_pin_gong_fa(self):
        diff = (407, 495, 88, 319)
        return self.calculate_relative_coords(diff)
    
    def jue_ping_gong_fa(self):
        diff = (610, 508, 80, 309)
        return self.calculate_relative_coords(diff)
    
    def xian_pin_gong_fa(self):
        diff = (810, 506, 86, 308)
        return self.calculate_relative_coords(diff)
        

class UseDaoJuExecutor(BaseExecutor):
    def __init__(self, usdj_coords_manager: UseDaoJuCoordsManager):
        super().__init__(usdj_coords_manager)
        self.usdj_coords_manager = usdj_coords_manager
        self.cat_dir = 'use_dao_ju'

    @wait_region
    def get_role_use_coords(self, wait_time, target_region, is_to_click, click_wait_time, to_raise_exception):
        return get_region_coords(
            'role_use',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_gong_fa_use_coords(self, wait_time, target_region, is_to_click, click_wait_time, to_raise_exception):
        return get_region_coords(
            'gong_fa_use',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_ling_shou_use_coords(self, wait_time, target_region, is_to_click, click_wait_time, to_raise_exception):
        return get_region_coords(
            'ling_shou_use',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_shen_yan_use_coords(self, wait_time, target_region, is_to_click, click_wait_time, to_raise_exception):
        return get_region_coords(
            'shen_yan_use',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_role_ling_gen_coords(self, wait_time, target_region, is_to_click, click_wait_time, to_raise_exception):
        return get_region_coords(
            'role_ling_gen',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_ling_wu_coords(self, wait_time, target_region, is_to_click, click_wait_time, to_raise_exception):
        return get_region_coords(
            'ling_wu',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_bu_tian_ling_zhu_not_enough_coords(self, wait_time, target_region, is_to_click, click_wait_time, to_raise_exception):
        return get_region_coords(
            'bu_tian_ling_zhu_not_enough',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_shu_xing_coords(self, wait_time, target_region, is_to_click, click_wait_time, to_raise_exception):
        return get_region_coords(
            'shu_xing',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_san_huang_ling_wei_ling_wu_coords(self, wait_time, target_region, is_to_click, click_wait_time, to_raise_exception):
        return get_region_coords(
            'san_huang_ling_wei_ling_wu',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_ling_wei_not_enough_coords(self, wait_time, target_region, is_to_click, click_wait_time, to_raise_exception):
        return get_region_coords(
            'ling_wei_not_enough',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_go_back_coords(self, wait_time, target_region, is_to_click, click_wait_time, to_raise_exception):
        return get_region_coords(
            'go_back',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_gong_fa_use_icon_coords(self, wait_time, target_region, is_to_click, click_wait_time, to_raise_exception):
        return get_region_coords(
            'gong_fa_use_icon',
            main_region_coords=self.usdj_coords_manager.profession_gong_fa_region(),
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
    
    def scroll_to_top(self, scroll_start_point_coords, scroll_length, scroll_seconds, scroll_times=5):
        pyautogui.moveTo(scroll_start_point_coords)
        scroll_length = self.calculate_scroll_length(scroll_length)
        for _ in range(scroll_times):
            scroll_specific_length(scroll_length, scroll_seconds)

    @wait_region
    def get_rong_he_coords(self, wait_time, target_region, is_to_click, click_wait_time, to_raise_exception):
        return get_region_coords(
            'rong_he',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_rong_he_over_coords(self, wait_time, target_region, is_to_click, click_wait_time, to_raise_exception):
        return get_region_coords(
            'rong_he_over',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_cang_shu_coords(self, wait_time, target_region, is_to_click, click_wait_time, to_raise_exception):
        return get_region_coords(
            'cang_shu',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_qi_dong_coords(self, wait_time, target_region, is_to_click, click_wait_time, to_raise_exception):
        return get_region_coords(
            'qi_dong',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_cang_shu_page_coords(self, wait_time, target_region, is_to_click, click_wait_time, to_raise_exception):
        shou_ling_icon_imgs = [
            {'target_region_image': 'shang_pin_gong_fa', 'main_region_coords': self.main_region_coords, 'confidence': 0.8, 'cat_dir': self.cat_dir},
            {'target_region_image': 'zhen_pin_gong_fa', 'main_region_coords': self.main_region_coords, 'confidence': 0.8, 'cat_dir': self.cat_dir},
            {'target_region_image': 'jue_pin_gong_fa', 'main_region_coords': self.main_region_coords, 'confidence': 0.8, 'cat_dir': self.cat_dir},
            {'target_region_image': 'xian_pin_gong_fa', 'main_region_coords': self.main_region_coords, 'confidence': 0.8, 'cat_dir': self.cat_dir},
        ]
        return get_region_coords_by_multi_imgs(shou_ling_icon_imgs)
    
    @wait_region
    def get_gong_fa_shu_coords(self, wait_time, target_region, is_to_click, click_wait_time, to_raise_exception):
        return get_region_coords(
            'gong_fa_shu',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )

    def use_role(self):

        self.go_to_world()

        click_region(self.usdj_coords_manager.small_xiu_lian(), seconds=4)
        click_region(self.usdj_coords_manager.expand_menu())

        role_use_coords = self.get_role_use_coords(wait_time=3, target_region="使用角色道具", is_to_click=True, click_wait_time=2, to_raise_exception=False)
        if role_use_coords is None:
            return
        
        # 使用补天灵根
        role_ling_gen_coords = self.get_role_ling_gen_coords(wait_time=3, target_region="使用灵根", is_to_click=True, click_wait_time=2, to_raise_exception=False)
        if role_ling_gen_coords is not None:
            ling_wu_coords = self.get_ling_wu_coords(wait_time=3, target_region="领悟", is_to_click=False, click_wait_time=2, to_raise_exception=False)
            if ling_wu_coords is not None:
                pyautogui.moveTo(calculate_center_coords(ling_wu_coords))
                pyautogui.mouseDown()

                while True:
                    bu_tian_ling_zhu_not_enough_coords = self.get_bu_tian_ling_zhu_not_enough_coords(
                        wait_time=2, target_region="补天灵珠不足", is_to_click=False, click_wait_time=1, to_raise_exception=False
                    )
                    if bu_tian_ling_zhu_not_enough_coords is not None:
                        pyautogui.mouseUp()
                        click_region(self.usdj_coords_manager.better_exit(), seconds=1)
                        break

        # 三皇灵威
        shu_xing_coords = self.get_shu_xing_coords(wait_time=3, target_region="属性", is_to_click=True, click_wait_time=2, to_raise_exception=False)
        if shu_xing_coords is not None:
            click_region(self.usdj_coords_manager.san_huang_ling_wei())
            san_huang_ling_wei_ling_wu_coords = self.get_san_huang_ling_wei_ling_wu_coords(wait_time=3, target_region="领悟", is_to_click=False, click_wait_time=2, to_raise_exception=False)
            if san_huang_ling_wei_ling_wu_coords is not None:
                pyautogui.moveTo(calculate_center_coords(san_huang_ling_wei_ling_wu_coords))

                while True:
                    for _ in range(3):
                        click_region(san_huang_ling_wei_ling_wu_coords, seconds=0)

                    ling_wei_not_enough_coords = self.get_ling_wei_not_enough_coords(
                        wait_time=2, target_region="灵威不足", is_to_click=False, click_wait_time=1, to_raise_exception=False
                    )
                    if ling_wei_not_enough_coords is not None:
                        click_region(self.usdj_coords_manager.better_exit(), seconds=1)
                        self.get_go_back_coords(wait_time=3, target_region="返回", is_to_click=True, click_wait_time=1, to_raise_exception=True)
                        break
    
    def use_gong_fa_cang_shu(self):
        cang_shu_coords = self.get_cang_shu_coords(wait_time=3, target_region="藏书", is_to_click=True, click_wait_time=2, to_raise_exception=False)
        if cang_shu_coords is None:
            return
        
        multi_gong_fa_coords = [
            self.usdj_coords_manager.shang_pin_gong_fa(),
            self.usdj_coords_manager.zhen_pin_gong_fa(),
            self.usdj_coords_manager.jue_ping_gong_fa(),
            self.usdj_coords_manager.xian_pin_gong_fa(),
        ]

        for gong_fa_coords in multi_gong_fa_coords:
            click_region(gong_fa_coords)
            qi_dong_coords = self.get_qi_dong_coords(wait_time=3, target_region="启动", is_to_click=False, click_wait_time=0, to_raise_exception=False)
            if qi_dong_coords is None:
                click_region(self.usdj_coords_manager.better_exit(), seconds=2)
                continue

            while True:
                for _  in range(5):
                    click_region(qi_dong_coords, seconds=0)

                cang_shu_page_coords = self.get_cang_shu_page_coords(wait_time=2, target_region="藏书页面", is_to_click=False, click_wait_time=2, to_raise_exception=False)
                if cang_shu_page_coords is not None:
                    break
        
        click_region(self.usdj_coords_manager.better_exit(), seconds=1)

    def use_gong_fa(self):

        self.go_to_world()

        click_region(self.usdj_coords_manager.small_xiu_lian(), seconds=4)
        click_region(self.usdj_coords_manager.expand_menu())
        
        gong_fa_use_coords = self.get_gong_fa_use_coords(wait_time=3, target_region="使用功法", is_to_click=True, click_wait_time=2, to_raise_exception=False)
        if gong_fa_use_coords is None:
            return
        
        self.get_gong_fa_shu_coords(wait_time=3, target_region="功法书", is_to_click=True, click_wait_time=2, to_raise_exception=False)

        while True:
            gong_fa_use_icon_coords = self.get_gong_fa_use_icon_coords(wait_time=3, target_region="使用功法", is_to_click=True, click_wait_time=2, to_raise_exception=False)
            if gong_fa_use_icon_coords is None:
                break

            click_region(gong_fa_use_icon_coords, seconds=1)

            self.scroll_to_top(
                scroll_start_point_coords=self.usdj_coords_manager.scroll_start_point()[:2],
                scroll_length=self.calculate_scroll_length(1000),
                scroll_seconds=1,
                scroll_times=10
            )

            while True:
                try:
                    self.scroll_and_click_by_multiple_imgs(
                        direction='down',
                        targets_imgs_info=[
                            {'target_region_image': 'ke_rong_he_1', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'cat_dir': self.cat_dir},
                            {'target_region_image': 'ke_rong_he_2', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'cat_dir': self.cat_dir},
                            {'target_region_image': 'ke_rong_he_3', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'cat_dir': self.cat_dir},
                        ],
                        target_name='可融合',
                        num_of_scroll=6,
                    )
                except Exception as e:
                    print(e)
                    break

                while True:
                    self.get_rong_he_coords(wait_time=3, target_region="融合", is_to_click=True, click_wait_time=1, to_raise_exception=True)
                    
                    rong_he_over_coords = self.get_rong_he_over_coords(wait_time=3, target_region="融合完成", is_to_click=False, click_wait_time=2, to_raise_exception=False)
                    if rong_he_over_coords is not None:
                        for _ in range(2):
                            click_region(self.usdj_coords_manager.better_exit(), seconds=1)
                        break
                    
                    click_region(self.usdj_coords_manager.better_exit(), seconds=1)

        # 藏书阁
        self.use_gong_fa_cang_shu()

    def use_fa_bao(self):
        pass

    def use_ling_shou(self):
        pass

    def use_shen_yan(self):
        pass
    
    def execute(self):
        
        self.go_to_world()

        # self.use_role()
        
        self.use_gong_fa()

if __name__ == '__main__':

    resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)

    main_region_coords = get_game_page_coords(resolution = resolution)

    coords_manager = UseDaoJuCoordsManager(main_region_coords)
    executor = UseDaoJuExecutor(coords_manager)

    executor.execute()
