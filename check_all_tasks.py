import time
import pyautogui
import numpy as np
from typing import Tuple
from utils_adb import *
from coords_manager import BaseCoordsManager
from event_executor import BaseExecutor
from xiuxian_exception import *

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True


class CheckAllTasksCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)
    

class CheckAllTasksExecutor(BaseExecutor):
    def __init__(self, cat_coords_manager: CheckAllTasksCoordsManager):
        super().__init__(cat_coords_manager)
        self.cat_coords_manager = cat_coords_manager
        self.all_tasks = [
            'ling_shou',
            'youli',
            'fuben',
            'bai_zu_gong_feng',
            'shuangxiu',
            'xiu_lian',
            'tiao_zhan_xian_yuan',
            'zhui_mo_gu',
            'lun_dao',
            'bai_ye'
        ]
        
        self.cat_dir = "check_all_tasks"

    @wait_region
    def get_open_ling_shou_coords(self, wait_time, target_region, is_to_click):
        open_ling_shou_coords = get_region_coords(
            'open_ling_shou',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir
        )
        return open_ling_shou_coords

    def get_buy_times_not_enough_indicator_coords(self):

        buy_times_not_enough_indicator_imgs = [
            {'target_region_image': 'buy_times_not_enough1', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': self.cat_dir},
            {'target_region_image': 'buy_times_not_enough2', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': self.cat_dir},
        ]
        return get_region_coords_by_multi_imgs(buy_times_not_enough_indicator_imgs)

    def execute(self):

        self.go_to_world()

        self.click_ri_chang()
        
        all_tasks_check_state = {
            'ling_shou': False,
            'youli': False,
            'fuben': False,
            'bai_zu_gong_feng': False,
            'shuangxiu': False,
            'xiu_lian': False,
            'tiao_zhan_xian_yuan': False,
            'zhui_mo_gu': False,
            'lun_dao': False,
            'bai_ye': False
        }

        all_tasks_execute_state = {}
        num_of_scroll = 12
        for scroll_idx in range(1, num_of_scroll):
            
            if scroll_idx != 1:
                # pyautogui.moveTo(self.cat_coords_manager.scroll_start_point()[:2])
                # scroll_specific_length(self.calculate_scroll_length(-300))
                scroll_specific_length(
                    start_x=0.5,
                    end_x=0.5,
                    start_y=0.66,
                    end_y=0.33,
                    seconds=2,
                )

            for task in self.all_tasks:
                if all_tasks_check_state[task] is True:
                    continue
                
                if task != 'zhui_mo_gu':
                    task_coords = get_region_coords(
                        task,
                        main_region_coords=self.main_region_coords,
                        confidence=0.95,
                        cat_dir=self.cat_dir
                    )
                else:
                    task_coords = get_region_coords_by_multi_imgs([
                        {'target_region_image': 'zhui_mo_gu', 'main_region_coords': self.main_region_coords, 'confidence': 0.95, 'cat_dir': self.cat_dir},
                        {'target_region_image': 'zhui_mo_gu_ling_jie', 'main_region_coords': self.main_region_coords, 'confidence': 0.95, 'cat_dir': self.cat_dir},
                    ])

                if task_coords is not None:
                    task_height, task_width = 223, 933
                    task_height = task_height * self.coords_manager.y_ratio
                    task_height = int(round(task_height))
                    task_width = task_width * self.coords_manager.x_ratio
                    task_width = int(round(task_width))
                    full_target_coords = (task_coords[0], task_coords[1], task_width, task_height)

                    finished_indicator_coords = get_region_coords_by_multi_imgs([
                        {'target_region_image': 'finished_task', 'main_region_coords': full_target_coords, 'confidence': 0.8, 'cat_dir': self.cat_dir},
                        {'target_region_image': 'already_bought', 'main_region_coords': full_target_coords, 'confidence': 0.8, 'cat_dir': self.cat_dir},
                    ])

                    if finished_indicator_coords is not None:
                        print(f"{task} 已经完成!")
                        all_tasks_check_state[task] = True
                        all_tasks_execute_state[task] = False # False: 表示已经执行过了, 不需要再执行了
                        continue
        
        return all_tasks_execute_state

if __name__ == '__main__':

    resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)

    main_region_coords = get_game_page_coords(resolution = resolution)

    coords_manager = CheckAllTasksCoordsManager(main_region_coords)
    executor = CheckAllTasksExecutor(coords_manager)
    
    executor.execute()

