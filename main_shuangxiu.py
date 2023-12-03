import pyautogui
import numpy as np
from typing import Tuple
import time
from utils import get_region_coords, click_region, get_game_page_coords, cal_diff_between_regions, extract_int_from_image
from coords_manager import YouliCoordsManager, ShuangXiuCoordsManager, BaseCoordsManager
from event_runner import BaseExecutor
import pytesseract
import cv2
import re
from xiuxian_exception import *

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True

main_region_coords = get_game_page_coords()

coords_manager = ShuangXiuCoordsManager(main_region_coords)
main_region_coords = coords_manager.main_region_coords

class ShuangXiuExecutor(BaseExecutor):
    def __init__(
        self,
        shuangxiu_coords_manager: ShuangXiuCoordsManager,
    ):
        super().__init__(shuangxiu_coords_manager, 'shuangxiu')

        self.shuangxiu_coords_manager = shuangxiu_coords_manager
        self.shuangxiu_name_dict = {
            'dian_feng_pei_yuan': '颠凤培元',
            'chi_qing_zhou': '痴情咒',
            'liu_yu_lian_xin': '六欲练心'
        }
        self.gonfa_order = ['dian_feng_pei_yuan', 'liu_yu_lian_xin']
        self.main_region_coords = self.shuangxiu_coords_manager.main_region_coords
        
        self.back_coords = self.shuangxiu_coords_manager.back()

    def click_back(self):
        while self._check_is_in_world() is False:
            click_region(self.back_coords, seconds=3)
            print("完成: 点击返回按钮")

    def click_shuangxiu_gongfashu(self, gongfashu_name: str):
        gongfashu_coords = get_region_coords(
            gongfashu_name, 
            main_region_coords=self.main_region_coords, 
            confidence=0.9, 
            cat_dir='shuangxiu'
        )
        print(f"完成: 识别一次{gongfashu_name}位置")

        if gongfashu_coords is None:
            raise Exception(f"未找到{gongfashu_name}位置.")

        click_region(gongfashu_coords, seconds=3)
        print(f"完成: 点击{gongfashu_name}按钮")

    def execute(self):
        if self._check_is_in_world() is False:
            raise Exception("当前不在世界地图界面")

        self.click_ri_chang()
        self.scoll_and_click('shuangxiu')
        self.click_shuangxiu_gongfashu('dian_feng_pei_yuan')
        self.click_back()
        

shuangxiu_executor = ShuangXiuExecutor(coords_manager)

shuangxiu_executor.execute()
