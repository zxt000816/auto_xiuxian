import pyautogui
import numpy as np
from typing import Tuple

from utils_adb import *
from coords_manager import BaseCoordsManager
from event_executor import BaseExecutor

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True

class AssistantCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords: tuple, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)
    
    def run_button(self, sub_main_coords: tuple):
        diff = (738, 39, 123, 129)
        return self.calculate_relative_coords(diff, sub_main_coords)
    
    def duihuan_run_button(self):
        diff = (218, 1226, 306, 98)
        return self.calculate_relative_coords(diff)
    
    def menu_expansion(self):
        diff = (976, 1743, 52, 54)
        return self.calculate_relative_coords(diff)
    
    def dao_yi_region(self):
        diff = (105, 419, 889, 208)
        return self.calculate_relative_coords(diff)
    
    def shen_wu_yuan_region(self):
        diff = (105, 670, 889, 208)
        return self.calculate_relative_coords(diff)

    def zong_men_zhu_shou_region(self):
        diff = (104, 923, 889, 208)
        return self.calculate_relative_coords(diff)

    def better_exit(self):
        diff = (370, 1844, 0, 0)
        return self.calculate_relative_coords(diff)

class AssistantExecutor(BaseExecutor):
    def __init__(self, assistant_coords_manager: AssistantCoordsManager):
        super().__init__(assistant_coords_manager, 'assistant')
        self.assistant_coords_manager = assistant_coords_manager
        self.task_order = ['zongmen', 'shenwuyuan', 'daoyi']
        self.task_name_dict = {
            'zongmen': '宗门助手',
            'shenwuyuan': '神物园助手',
            'daoyi': '道义秘库助手',
            'baiye': '拜谒'
        }

    def _check_is_in_assistant(self) -> bool:
        assistant_image_coords = get_region_coords(
            'assistant_list',
            main_region_coords=self.main_region_coords,
            confidence=0.9,
            cat_dir=self.cat_dir,
        )

        if assistant_image_coords is not None:
            return True
        else:
            return False

    def click_assistant(self):
        click_region(self.coords_manager.assistant(), seconds=3)
        print("完成: 点击小助手图标")

    def search_run_button_and_click(self, sub_main_coords: tuple):
        run_button_coords = self.assistant_coords_manager.run_button(sub_main_coords)
        click_region(run_button_coords, seconds=2)
        print("完成: 点击运行按钮")

    def process_duihuan_alert(self):
        duihuan_alert_coords = get_region_coords(
            'duihuan_alert',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir='assistant',
        )
        if duihuan_alert_coords is not None:
            click_region(self.assistant_coords_manager.duihuan_run_button(), seconds=2)
            print("完成: 点击兑换运行按钮")

    @wait_region
    def get_dui_huan_alert_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'duihuan_alert',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir='assistant',
        )

    def search_task_region_and_click(self, task: str):
        task_name = self.task_name_dict[task]
        task_image_coords = get_region_coords(
            task,
            main_region_coords=self.main_region_coords,
            confidence=0.9,
            cat_dir=self.cat_dir,
        )
        if task_image_coords is None:
            raise Exception(f"未找到{task_name}位置")

        self.search_run_button_and_click(task_image_coords)
        print(f"完成: 点击{task_name}运行按钮")

    @wait_region
    def get_task_coords(self, task, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            task,
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir,
        )

    @wait_region
    def get_zhi_xing_over_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'zhi_xing_over',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_dui_huan_alert_or_zhi_xing_over_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        imgs = [
            {'target_region_image': 'duihuan_alert', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': self.cat_dir},
            {'target_region_image': 'zhi_xing_over', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': self.cat_dir},
        ]
        return get_region_coords_by_multi_imgs(imgs)
    
    @wait_region
    def get_email_coords(self, wait_time, target_region, is_to_click, click_wait_time):
        return get_region_coords(
            'email',
            self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir
        )
    
    @wait_region
    def get_yi_jian_ling_qu_coords(self, wait_time, target_region, is_to_click, click_wait_time):
        return get_region_coords(
            'yi_jian_ling_qu',
            self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir
        )

    def execute(self):

        self.go_to_world()

        self.click_ri_chang()
        self.click_assistant()
        
        for task in self.task_order:
            try:
                if task == 'zongmen':
                    task_coords = self.assistant_coords_manager.zong_men_zhu_shou_region()
                elif task == 'shenwuyuan':
                    task_coords = self.assistant_coords_manager.shen_wu_yuan_region()
                elif task == 'daoyi':
                    task_coords = self.assistant_coords_manager.dao_yi_region()
                else:
                    raise Exception("未知任务")
                
                # task_coords = self.get_task_coords(task, wait_time=3, target_region=self.task_name_dict[task],
                #                                     is_to_click=False, to_raise_exception=False)
                # if task_coords is None:
                #     print(f"未找到{self.task_name_dict[task]}位置")
                #     continue
                
                self.search_run_button_and_click(task_coords)

                self.get_dui_huan_alert_coords(wait_time=3, target_region='仍要执行', is_to_click=True, to_raise_exception=False)

                self.get_zhi_xing_over_coords(wait_time=3, target_region='执行结束', is_to_click=True, to_raise_exception=False)
                
            except Exception as e:
                print(e)

        self.go_to_world()

        click_region(self.assistant_coords_manager.menu_expansion(), seconds=2)

        self.get_email_coords(wait_time=3, target_region='邮件', is_to_click=True, click_wait_time=2)

        self.get_yi_jian_ling_qu_coords(wait_time=3, target_region='一键领取', is_to_click=True, click_wait_time=2)

        click_region(self.assistant_coords_manager.better_exit())

if __name__ == '__main__':

    main_region_coords = get_game_page_coords()

    corrds_manager = AssistantCoordsManager(main_region_coords)
    
    executor = AssistantExecutor(corrds_manager)

    executor.execute()
