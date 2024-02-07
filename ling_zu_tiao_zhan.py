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
from utils_adb import get_region_coords, wait_region
from coords_manager import BaseCoordsManager
from event_executor import BaseExecutor

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True

class LingZuTiaoZhanCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)

    def all_xian_yuan(self):
        diff=(324, 280, 160, 80)
        return self.calculate_relative_coords(diff)
    
    def qian_wang(self):
        diff=(430, 1527, 255, 96)
        return self.calculate_relative_coords(diff)

class LingZuTiaoZhanExecutor(BaseExecutor):
    def __init__(self, lztz_coords_manager: LingZuTiaoZhanCoordsManager):
        super().__init__(lztz_coords_manager, 'ling_zu_tiao_zhan')
        self.lztz_coords_manager = lztz_coords_manager
        
    @wait_region
    def get_ling_zu_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        ling_zu_coords = get_region_coords(
            'ling_zu',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir
        )
        return ling_zu_coords
    
    @wait_region
    def get_qian_wang_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        qian_wang_coords = get_region_coords(
            'qian_wang',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir
        )
        return qian_wang_coords
    
    @wait_region
    def get_tiao_zhan_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        tiao_zhan_coords = get_region_coords(
            'tiao_zhan',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir
        )
        return tiao_zhan_coords

    @wait_region
    def get_start_tiao_zhan_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        start_tiao_zhan_coords = get_region_coords(
            'start_tiao_zhan',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir
        )
        return start_tiao_zhan_coords
    
    @wait_region
    def get_tiao_zhan_over_coords(self, wait_time, target_region, is_to_click, wait_time_before_click, to_raise_exception):
        tiao_zhan_over_coords = get_region_coords(
            'tiao_zhan_over',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir
        )
        return tiao_zhan_over_coords

    def execute(self):
        
        self.go_to_world()
        
        self.click_ri_chang()

        self.scroll_and_click(direction='down')

        self.get_ling_zu_coords(wait_time=5, target_region='灵祖', is_to_click=True, to_raise_exception=True)

        self.get_qian_wang_coords(wait_time=3, target_region='前往', is_to_click=True, to_raise_exception=True)    

        self.get_tiao_zhan_coords(wait_time=60, target_region='挑战', is_to_click=True, to_raise_exception=True)

        self.get_start_tiao_zhan_coords(wait_time=3, target_region='开始挑战', is_to_click=True, to_raise_exception=True)

        self.get_tiao_zhan_over_coords(wait_time=120, target_region='挑战结束', is_to_click=True, wait_time_before_click=3, to_raise_exception=True)


if __name__ == '__main__':

    lztz_coords_manager = LingZuTiaoZhanCoordsManager(main_region_coords, resolution=resolution)
    executor = LingZuTiaoZhanExecutor(lztz_coords_manager)
    executor.execute()
