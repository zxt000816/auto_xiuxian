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
from utils_adb import get_game_page_coords, get_region_coords, click_region, wait_region, get_region_coords_by_multi_imgs
from coords_manager import BaseCoordsManager
from event_executor import BaseExecutor

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True

class QiXiMoJieCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)

    def confirm_button_in_last_qi_xi_alert(self):
        diff = (391, 1252, 303, 97)
        return self.calculate_relative_coords(diff)
    
    def confirm_button_in_chuang_jian_dui_wu(self):
        diff = (607, 1188, 303, 94)
        return self.calculate_relative_coords(diff)

class QiXiMoJieExecutor(BaseExecutor):
    def __init__(self, qxmj_coords_manager: QiXiMoJieCoordsManager):
        super().__init__(qxmj_coords_manager, 'qi_xi_mo_jie')
        self.qxmj_coords_manager = qxmj_coords_manager

    @wait_region
    def get_last_qi_xi_alert(self, wait_time, target_region, is_to_click, other_region_coords, to_raise_exception):
        return get_region_coords(
            'last_qi_xi_alert',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_can_yu_jin_gong(self, wait_time, target_region, is_to_click, other_region_coords, to_raise_exception):
        return get_region_coords(
            'can_yu_jin_gong',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_kun_nan(self, wait_time, target_region, is_to_click, other_region_coords, to_raise_exception):
        kun_nan_imgs = [
            {'target_region_image': 'kun_nan1', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': self.cat_dir},
            {'target_region_image': 'kun_nan2', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': self.cat_dir},
        ]
        return get_region_coords_by_multi_imgs(kun_nan_imgs)
    
    @wait_region
    def get_chuang_jian_dui_wu_coords(self, wait_time, target_region, is_to_click, other_region_coords, to_raise_exception):
        return get_region_coords(
            'chuang_jian_dui_wu',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_chuang_jian_dui_wu_alert(self, wait_time, target_region, is_to_click, other_region_coords, to_raise_exception):
        return get_region_coords(
            'chuang_jian_dui_wu_alert',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_qi_xi_mo_jie_coords(self, wait_time, target_region, is_to_click, other_region_coords, to_raise_exception):
        return get_region_coords(
            'qi_xi_mo_jie',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_already_have_team_coords(self, wait_time, target_region, is_to_click, other_region_coords, to_raise_exception):
        return get_region_coords(
            'already_have_team',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir,
        )

    def execute(self):
        self.go_to_world()
        
        click_region(self.qxmj_coords_manager.ri_cheng())

        self.get_general_coords(wait_time=5, target_region='常规', is_to_click=True, to_raise_exception=True)

        self.get_qi_xi_mo_jie_coords(wait_time=5, target_region='奇袭魔界', is_to_click=True, other_region_coords=None, to_raise_exception=True)

        # self.scroll_and_click(direction='down', in_ri_chang_page=False) # 虽然在日常页面, 但因为奇袭魔界的完成, 并不是真正的完成, 需要进去进行判断.

        already_have_team_coords = self.get_already_have_team_coords(wait_time=3, target_region='已有队伍', is_to_click=False, other_region_coords=None, to_raise_exception=False)
        if already_have_team_coords is not None:
            print('已有队伍, 说明奇袭魔界已经完成, 退出!')
            return

        self.get_last_qi_xi_alert(wait_time=3, target_region='上次奇袭魔界提示框', is_to_click=True, 
                                    other_region_coords=self.qxmj_coords_manager.confirm_button_in_last_qi_xi_alert(), to_raise_exception=False)

        self.get_can_yu_jin_gong(wait_time=5, target_region='参与进攻', is_to_click=True, other_region_coords=None, to_raise_exception=True)

        self.get_kun_nan(wait_time=5, target_region='困难', is_to_click=True, other_region_coords=None, to_raise_exception=True)

        self.get_chuang_jian_dui_wu_coords(wait_time=3, target_region='创建队伍', is_to_click=True, other_region_coords=None, to_raise_exception=True)

        self.get_chuang_jian_dui_wu_alert(wait_time=3, target_region='创建队伍提示框', is_to_click=True, 
                                            other_region_coords=self.qxmj_coords_manager.confirm_button_in_chuang_jian_dui_wu(), to_raise_exception=True)


if __name__ == "__main__":
    

    # main_region_coords = get_game_page_coords(resolution = resolution)

    coords_manager = QiXiMoJieCoordsManager(main_region_coords, resolution=resolution)

    executor = QiXiMoJieExecutor(coords_manager)

    executor.execute()
