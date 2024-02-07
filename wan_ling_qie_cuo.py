# import os
# import adbutils

# adb = adbutils.AdbClient(host="127.0.0.1", port=5037)

# serial = "emulator-5566"
# device = adb.device(serial=serial)

# resolution = (540, 960)
# os.environ['DEVICE_SERIAL'] = serial
# os.environ['ROOT_DIR'] = f'FanRenXiuXianIcon_{resolution[0]}_{resolution[1]}'

# main_region_coords = (1364, 47, 540, 960)

# os.environ['MAIN_REGION_COORDS'] = ','.join(map(str, main_region_coords))

import time
import pyautogui
from utils_adb import get_region_coords, wait_region, click_region
from coords_manager import BaseCoordsManager
from event_executor import BaseExecutor

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True

class WanLingQieCuoCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)

class WanLingQieCuoExecutor(BaseExecutor):
    def __init__(self, wlqc_coords_manager: WanLingQieCuoCoordsManager):
        super().__init__(wlqc_coords_manager, 'wan_ling_qie_cuo')
        self.wlqc_coords_manager = wlqc_coords_manager
        
    @wait_region
    def get_yu_wai_mo_ling_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        yu_wai_mo_ling_coords = get_region_coords(
            'yu_wai_mo_ling',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir
        )
        return yu_wai_mo_ling_coords
    
    @wait_region
    def get_qie_cuo_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        qie_cuo_coords = get_region_coords(
            'qie_cuo',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir
        )
        return qie_cuo_coords
    
    @wait_region
    def get_yao_qing_ling_ti_1_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        yao_qing_ling_ti_coords = get_region_coords(
            'yao_qing_ling_ti_1',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir
        )
        return yao_qing_ling_ti_coords
    
    @wait_region
    def get_yao_qing_ling_ti_2_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        yao_qing_ling_ti_coords = get_region_coords(
            'yao_qing_ling_ti_2',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir
        )
        return yao_qing_ling_ti_coords
    
    @wait_region
    def get_ling_ti_page_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        ling_ti_page_coords = get_region_coords(
            'ling_ti_page',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir
        )
        return ling_ti_page_coords
    
    @wait_region
    def get_yao_qing_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        yao_qing_coords = get_region_coords(
            'yao_qing',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir
        )
        return yao_qing_coords
    
    @wait_region
    def get_disabled_checkbox_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        disabled_checkbox_coords = get_region_coords(
            'disabled_checkbox',
            main_region_coords=self.main_region_coords,
            confidence=0.9,
            cat_dir=self.cat_dir
        )
        return disabled_checkbox_coords
    
    @wait_region
    def get_qian_wang_qie_cuo_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        qian_wang_qie_cuo_coords = get_region_coords(
            'qian_wang_qie_cuo',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir
        )
        return qian_wang_qie_cuo_coords
    
    @wait_region
    def get_qie_cuo_over(self, wait_time, target_region, is_to_click, to_raise_exception):
        qie_cuo_over_coords = get_region_coords(
            'qie_cuo_over',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir
        )
        return qie_cuo_over_coords

    @wait_region
    def get_shi_yong_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        shi_yong_coords = get_region_coords(
            'shi_yong',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir
        )
        return shi_yong_coords

    def execute(self, index=0):
        
        if index == 0:

            self.go_to_world()
            
            self.click_ri_chang()

            self.scroll_and_click(direction='down', in_ri_chang_page=False)

            self.get_yu_wai_mo_ling_coords(wait_time=5, target_region="域外魔灵", is_to_click=True, to_raise_exception=True)

            self.get_qie_cuo_coords(wait_time=3, target_region="切磋", is_to_click=True, to_raise_exception=True)

            self.get_yao_qing_ling_ti_1_coords(wait_time=3, target_region="邀请灵体1", is_to_click=True, to_raise_exception=True)

        self.get_yao_qing_ling_ti_2_coords(wait_time=3, target_region="邀请灵体2", is_to_click=True, to_raise_exception=False)

        self.get_ling_ti_page_coords(wait_time=3, target_region="灵体页面", is_to_click=True, to_raise_exception=True)

        self.get_yao_qing_coords(wait_time=3, target_region="邀请", is_to_click=True, to_raise_exception=True)

        if index == 0:
            while True:
                disabled_checkbox_coords = self.get_disabled_checkbox_coords(
                    wait_time=3, 
                    target_region="checkbox", 
                    is_to_click=True, 
                    to_raise_exception=False
                )

                if disabled_checkbox_coords is None:
                    break

        self.get_qian_wang_qie_cuo_coords(wait_time=3, target_region="前往切磋", is_to_click=True, to_raise_exception=True)

        shi_yong_coords = self.get_shi_yong_coords(wait_time=3, target_region="使用", is_to_click=True, to_raise_exception=False)
        if shi_yong_coords is not None:
            self.get_qian_wang_qie_cuo_coords(wait_time=3, target_region="前往切磋", is_to_click=True, to_raise_exception=True)

        qie_cuo_over_coords = self.get_qie_cuo_over(wait_time=3, target_region="切磋结束", is_to_click=False, to_raise_exception=False)
        if qie_cuo_over_coords is not None:
            print("切磋结束")
            click_region(self.wlqc_coords_manager.better_exit())    
            return

        click_region(self.wlqc_coords_manager.better_exit())

        return self.execute(index=index+1)

if __name__ == '__main__':

    wlqc_coords_manager = WanLingQieCuoCoordsManager(main_region_coords, resolution=resolution)
    executor = WanLingQieCuoExecutor(wlqc_coords_manager)
    executor.execute()