import pyautogui
import time
import numpy as np
from typing import Tuple
from utils import get_game_page_coords, get_region_coords, get_region_coords_by_multi_imgs, click_region
from coords_manager import BaseCoordsManager
from event_executor import BaseExecutor

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True

class HongBaoCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords: tuple, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)

    def chat_page(self):
        diff = (610, 1665, 170, 80)
        return self.calculate_relative_coords(diff)

class HongBaoExecutor(BaseExecutor):
    def __init__(self, hong_bao_coords_manager: HongBaoCoordsManager):
        super().__init__(hong_bao_coords_manager, 'hong_bao')
        self.hong_bao_coords_manager = hong_bao_coords_manager

    def get_hon_bao_coords(self):
        hong_bao_alert_coords = get_region_coords(
            'hong_bao',
            main_region_coords=self.hong_bao_coords_manager.main_region_coords,
            confidence=0.8,
            cat_dir='hong_bao',
        )
        return hong_bao_alert_coords

    def get_open_hong_bao_coords(self):
        open_hong_bao_coords = get_region_coords(
            'open_hong_bao',
            main_region_coords=self.hong_bao_coords_manager.main_region_coords,
            confidence=0.8,
            cat_dir='hong_bao',
        )
        return open_hong_bao_coords
    
    def get_next(self):
        next_coords = get_region_coords(
            'next',
            main_region_coords=self.hong_bao_coords_manager.main_region_coords,
            confidence=0.8,
            cat_dir='hong_bao',
        )
        return next_coords
    
    def get_ling_shi_hong_bao_coords(self):
        ling_shi_hong_bao_imgs = [
            {'target_region_image': 'ling_shi_hong_bao2', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': self.cat_dir},
            {'target_region_image': 'ling_shi_hong_bao1', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': self.cat_dir},
        ]
        return get_region_coords_by_multi_imgs(ling_shi_hong_bao_imgs)

    def start_ling_qu_hong_bao(self):
        # 开始领取红包
        while True:
            # 获取并点击红包打开按钮
            open_hong_bao_coords = self.get_open_hong_bao_coords()
            if not self.click_if_coords_exist(open_hong_bao_coords, message='检测到红包打开按钮'):
                print('没有检测到红包打开按钮，可能已经领完了')
                break
            
            # 红包打开后，点击下一个红包
            next_coords = self.get_next()
            if not self.click_if_coords_exist(next_coords, message='检测到下一个红包'):
                print('没有检测到下一个红包，可能已经领完了')
                break

    def execute(self):
        self.go_to_world()

        # 点击聊天框
        click_region(self.hong_bao_coords_manager.chat(), seconds=3)
        click_region(self.hong_bao_coords_manager.chat_page())

        # 滚动到包含红包的对话
        start_time = time.time()
        while True:
            if time.time() - start_time > 120:
                print('滚动超时，退出')
                break

            self.scroll_and_click(direction='down', other_target='hong_bao', other_target_name='红包', num_of_scroll=3)

            hong_bao_coords = self.get_hon_bao_coords()
            if not self.click_if_coords_exist(hong_bao_coords, message='检测到红包'):
                print('没有检测到红包，可能已经领完了')
                break
            
            ling_shi_hong_bao_coords = self.get_ling_shi_hong_bao_coords()
            click_region(ling_shi_hong_bao_coords)
            
            self.start_ling_qu_hong_bao()
            # 点击指定返回坐标点两次, 返回到对话列表界面
            click_region(self.hong_bao_coords_manager.exit(), seconds=2)
            click_region(self.hong_bao_coords_manager.exit(), seconds=2)

if __name__ == '__main__':

    resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)

    main_region_coords = get_game_page_coords(resolution = resolution)

    hong_bao_coords_manager = HongBaoCoordsManager(main_region_coords, resolution=resolution)
    hong_bao_executor = HongBaoExecutor(hong_bao_coords_manager)

    hong_bao_executor.execute()
