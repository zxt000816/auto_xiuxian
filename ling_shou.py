import time
import pyautogui
from utils_adb import *
from coords_manager import BaseCoordsManager
from event_executor import BaseExecutor
from game_control import GameControlCoordsManager, GameControlExecutor
from xiuxian_exception import *

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True

class LingShouCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)

    def region_for_check_mutli_challenge(self):
        diff = (449, 1705, 77, 69)
        return self.calculate_relative_coords(diff)

class LingShouExecutor(BaseExecutor):
    def __init__(self, ls_coords_manager: LingShouCoordsManager, buy_times: int, to_save_times: bool = True):
        super().__init__(ls_coords_manager, 'ling_shou')
        self.ls_coords_manager = ls_coords_manager
        self.buy_times = buy_times
        self.finish_buying_times = False
        self.to_save_times = to_save_times
        self.challenge_times = 2

    @wait_region
    def get_open_ling_shou_coords(self, wait_time, target_region, is_to_click):
        open_ling_shou_coords = get_region_coords(
            'open_ling_shou',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir
        )
        return open_ling_shou_coords
    
    @wait_region
    def get_tui_jian_coords(self, wait_time, target_region, is_to_click):
        tui_jian_coords = get_region_coords(
            'tui_jian',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir
        )
        return tui_jian_coords

    def get_multi_challenge_auth_coords(self):
        multi_challenge_auth_coords = get_region_coords(
            'multi_challenge_auth',
            main_region_coords=self.main_region_coords,
            confidence=0.9,
            cat_dir=self.cat_dir
        )
        return multi_challenge_auth_coords
    
    @click_if_coords_exist
    def get_buy_times_icon_coords(self, target_region):
        buy_times_icon_coords = get_region_coords(
            'buy_times_icon',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir
        )
        return buy_times_icon_coords
    
    @wait_region
    def get_qian_wang_jiao_mie_coords(self, wait_time, target_region, is_to_click):
        qian_wang_jiao_mie_coords = get_region_coords(
            'qian_wang_jiao_mie',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir
        )
        return qian_wang_jiao_mie_coords

    @wait_region
    def get_jiao_mie_over_coords(self, wait_time, target_region, is_to_click):
        jiao_mie_over_coords = get_region_coords(
            'jiao_mie_over',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir
        )
        return jiao_mie_over_coords
    
    @wait_region
    def get_ling_shou_fu_ben_enter_coords(self, wait_time, target_region, is_to_click):
        ling_shou_fu_ben_enter_coords = get_region_coords(
            'ling_shou_fu_ben_enter',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir
        )
        return ling_shou_fu_ben_enter_coords

    def get_buy_times_not_enough_indicator_coords(self):
        buy_times_not_enough_indicator_imgs = [
            {'target_region_image': 'buy_times_not_enough1', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'cat_dir': self.cat_dir},
            {'target_region_image': 'buy_times_not_enough2', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'cat_dir': self.cat_dir},
        ]
        return get_region_coords_by_multi_imgs(buy_times_not_enough_indicator_imgs)
    
    @wait_region
    def get_kuai_su_sao_dang_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        kuai_su_sao_dang_coords = get_region_coords(
            'kuai_su_sao_dang',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir
        )
        return kuai_su_sao_dang_coords

    def execute(self, i=0):
        self.go_to_world()
        
        self.click_ri_chang()
        self.scroll_and_click(direction='down', confidence=0.95)

        self.get_open_ling_shou_coords(wait_time=120, target_region='灵兽界面', is_to_click=False)
        self.get_tui_jian_coords(wait_time=10, target_region='推荐剿灭', is_to_click=True)

        # 如果要存储次数, 那么就要关掉多人挑战, 否则就打开
        # multi_challenge_auth_coords = self.get_multi_challenge_auth_coords()
        # if self.to_save_times:
        #     if multi_challenge_auth_coords is not None:
        #         self.open_or_close_checkbox(
        #             operation='close', 
        #             target_region=self.ls_coords_manager.region_for_check_mutli_challenge()
        #         )
        #     else:
        #         print("完成: 该账号没有多人挑战的权限!")

        # if multi_challenge_auth_coords is not None:
        #     self.open_or_close_checkbox(
        #         operation='close', 
        #         target_region=self.ls_coords_manager.region_for_check_mutli_challenge()
        #     )
        # else:
        #     print("完成: 该账号没有多人挑战的权限!")

        if self.finish_buying_times is False:
            self.get_buy_times_icon_coords(target_region='购买次数图标')
            actual_buy_times = self.buy_times_in_store(self.buy_times, 'buy_times_not_enough1')
            self.challenge_times = self.challenge_times + actual_buy_times

        print(f"完成: 总共挑战次数为{self.challenge_times}次!")

        kuai_su_sao_dang_coords = self.get_kuai_su_sao_dang_coords(wait_time=3, target_region='快速扫荡', is_to_click=False, to_raise_exception=False)
        if kuai_su_sao_dang_coords is not None:
            print("完成: 已经开启快速扫荡!")
            self.get_qian_wang_jiao_mie_coords(wait_time=10, target_region='前往剿灭', is_to_click=True)

        # 如果不存储次数, 那么将购买的次数加到挑战次数上
        # if self.to_save_times is False:
            # self.challenge_times = self.challenge_times + actual_buy_times

        # print(f"完成: 总共挑战次数为{self.challenge_times}次!")
        # for i in range(self.challenge_times):
        #     print(f"完成: 开始第{i + 1}次剿灭!")
        #     self.get_qian_wang_jiao_mie_coords(wait_time=10, target_region='前往剿灭', is_to_click=True)
        #     if self.get_buy_times_not_enough_indicator_coords() is not None:
        #         print("完成: 挑战次数不足!")
        #         break

        #     self.get_jiao_mie_over_coords(wait_time=120, target_region='剿灭结束', is_to_click=True)

        #     if i == self.challenge_times - 1:
        #         print("完成: 所有次数已用完!")
        #         break

        #     self.get_ling_shou_fu_ben_enter_coords(wait_time=120, target_region='灵兽副本进入', is_to_click=True)
        #     self.get_open_ling_shou_coords(wait_time=120, target_region='灵兽界面', is_to_click=False)
        #     self.get_tui_jian_coords(wait_time=10, target_region='推荐剿灭', is_to_click=True)
        
        print(f"完成: 开始第{i + 1}次剿灭!")
        self.get_qian_wang_jiao_mie_coords(wait_time=10, target_region='前往剿灭', is_to_click=True)
        if self.get_buy_times_not_enough_indicator_coords() is not None:
            print("完成: 挑战次数不足!")
            return

        self.get_jiao_mie_over_coords(wait_time=120, target_region='剿灭结束', is_to_click=True)

        if i + 1 == self.challenge_times:
            print("完成: 所有次数已用完!")
            return

        # self.get_ling_shou_fu_ben_enter_coords(wait_time=120, target_region='灵兽副本进入', is_to_click=True)
        # self.get_open_ling_shou_coords(wait_time=120, target_region='灵兽界面', is_to_click=False)
        # self.get_tui_jian_coords(wait_time=10, target_region='推荐剿灭', is_to_click=True)

        time.sleep(4)
        return self.execute(i + 1)

if __name__ == '__main__':

    resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)

    main_region_coords = get_game_page_coords(resolution = resolution)

    gc_cm = GameControlCoordsManager(main_region_coords)

    gc_executor = GameControlExecutor(
        gc_cm, 
        account_name='白起(黄河)', 
        account='jbzd8a8fe8db',
        server='黄河入海'
    )
    gc_executor.execute()

    coords_manager = LingShouCoordsManager(main_region_coords)
    executor = LingShouExecutor(coords_manager, buy_times=1, to_save_times=False)
    
    executor.execute()

