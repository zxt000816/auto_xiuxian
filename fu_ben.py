import pyautogui
import numpy as np
from typing import Tuple
from utils import *
from coords_manager import BaseCoordsManager
from event_executor import BaseExecutor

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True
resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)

class FuBenCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)

    def buy_times_button(self):
        diff = (695, 1525, 61, 58)
        return self.calculate_relative_coords(diff)

    def zu_dui_alert_confirm(self):
        # 组队界面-确认按钮
        diff = (405, 1261, 311, 111)
        return self.calculate_relative_coords(diff)
    
    def fen_shen_page(self):
        # 邀请界面-分身
        diff = (322, 391, 136, 85)
        return self.calculate_relative_coords(diff)
    
    def real_tiao_zhan_times(self):
        # 副本界面-实际挑战次数
        diff = (617, 1538, 22, 37)
        return self.calculate_relative_coords(diff)
    
    def region_for_check_multi_challenge(self):
        # 副本界面-检查多人挑战图标是否存在的区域
        diff = (503, 1702, 65, 61)
        return self.calculate_relative_coords(diff)

class FuBenExecutor(BaseExecutor):
    def __init__(
        self, 
        fb_coords_manager: FuBenCoordsManager, 
        fuben_name: str,
        buy_times=3,
        to_save_times: bool=False,
    ):
        super().__init__(fb_coords_manager, 'fuben')
        self.fb_coords_manager = fb_coords_manager
        self.fuben_name = fuben_name
        self.buy_times = buy_times
        self.fuben_name_dict = {
            '广寒界': 'guang_han_jie',
            '昆吾山': 'kun_wu_shan',
            '天澜圣殿': 'tian_lan_sheng_dian',
            '深海巢穴': 'shen_hai_chao_xue',
            '越国皇宫': 'yue_guo_huang_gong',
            '血色禁地': 'xue_se_jin_di',
        }
        self.fuben = self.fuben_name_dict[fuben_name]
        self.finish_buying_times = False
        self.challenge_times = 3
        self.to_save_times = to_save_times


    @wait_region
    def get_zui_dui_coords(self, wait_time, target_region, is_to_click):
        return get_region_coords(
            'zu_dui',
            self.main_region_coords,
            confidence=0.9,
            grayscale=True,
            cat_dir=self.cat_dir
        )
    
    def get_multi_challenge_auth_coords(self):
        multi_challenge_auth_coords = get_region_coords(
            'multi_challenge_auth',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir
        )
        return multi_challenge_auth_coords

    def get_tiao_zhan_coords(self):
        return get_region_coords(
            'tiao_zhan',
            self.main_region_coords,
            confidence=0.8,
            grayscale=True,
            cat_dir=self.cat_dir
        )
    
    @wait_region
    def get_chuang_jian_dui_wu_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'chuang_jian_dui_wu',
            self.main_region_coords,
            confidence=0.8,
            grayscale=True,
            cat_dir=self.cat_dir
        )

    @wait_region
    def get_zu_dui_alert_coords(self, wait_time, target_region, is_to_click):
        return get_region_coords(
            'zu_dui_alert',
            self.main_region_coords,
            confidence=0.8,
            grayscale=True,
            cat_dir=self.cat_dir
        )
    
    @wait_region
    def get_confirm_in_zu_dui_alert_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'confirm_in_zu_dui_alert',
            self.main_region_coords,
            confidence=0.7,
            grayscale=False,
            cat_dir=self.cat_dir
        )

    @wait_region
    def get_yao_qing_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'yao_qing',
            self.main_region_coords,
            confidence=0.8,
            grayscale=True,
            cat_dir=self.cat_dir
        )

    @wait_region
    def get_yao_qing_fen_shen(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'yao_qing_fen_shen',
            self.main_region_coords,
            confidence=0.8,
            grayscale=True,
            cat_dir=self.cat_dir
        )
    
    @wait_region
    def get_team_is_full(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'team_is_full',
            self.main_region_coords,
            confidence=0.7,
            grayscale=True,
            cat_dir=self.cat_dir
        )
    
    def zu_dui(self):
        self.get_zui_dui_coords(wait_time=3, target_region='组队按钮', is_to_click=True)

        self.get_chuang_jian_dui_wu_coords(wait_time=3, target_region='创建队伍按钮', is_to_click=True, to_raise_exception=False)

        self.get_confirm_in_zu_dui_alert_coords(wait_time=3, target_region='确认按钮', is_to_click=True, to_raise_exception=False) 

        self.get_yao_qing_coords(wait_time=2, target_region='邀请按钮', is_to_click=True, to_raise_exception=False)

        click_region(self.fb_coords_manager.fen_shen_page(), seconds=2)

        start_time = time.time()
        # 等待20秒
        while True:
            if time.time() - start_time > 20:
                break

            self.get_yao_qing_fen_shen(wait_time=3, target_region='分身按钮', is_to_click=True, to_raise_exception=False)
            team_is_full_coords = self.get_team_is_full(wait_time=2, target_region='队伍人满', is_to_click=False, to_raise_exception=False)

            if team_is_full_coords is not None:
                print("完成: 队伍人满!")
                break
        
        start_time = time.time()
        # 等待10秒
        while self.get_tiao_zhan_coords() is None:
            click_region(self.fb_coords_manager.exit(), seconds=2)

    def get_buy_times_not_enough(self):
        return get_region_coords(
            'buy_times_not_enough',
            self.main_region_coords,
            confidence=0.8,
            grayscale=True,
            cat_dir=self.cat_dir
        )
    
    @wait_region
    def get_tiao_zhan_over_coords(self, wait_time, target_region, is_to_click):
        return get_region_coords(
            'tiao_zhan_over',
            self.main_region_coords,
            confidence=0.8,
            grayscale=True,
            cat_dir=self.cat_dir
        )

    @click_if_coords_exist
    def get_buy_times_icon_coords(self, target_region):
        buy_times_icon_coords = get_region_coords(
            'buy_times_icon',
            self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir
        )
        return buy_times_icon_coords

    @wait_region
    def get_fu_ben_enter_coords(self, wait_time, target_region, is_to_click):
        return get_region_coords(
            f'{self.fuben}_enter',
            self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir
        )
    
    @wait_region
    def get_fu_ben_page_indicator_coords(self, wait_time, target_region, is_to_click):
        fu_ben_page_indicator_imgs = [
            {'target_region_image': 'fu_ben_page_indicator1', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'cat_dir': self.cat_dir},
            {'target_region_image': 'fu_ben_page_indicator2', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'cat_dir': self.cat_dir},
        ]
        return get_region_coords_by_multi_imgs(fu_ben_page_indicator_imgs)
    
    @wait_region
    def get_tiao_zhan_alert_coords(self, wait_time, target_region, is_to_click, wait_time_before_click, to_raise_exception):
        return get_region_coords(
            'tiao_zhan_alert',
            self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir
        )
        
    def get_times_not_enough(self):
        return get_region_coords(
            'wu_ci_shu_alert',
            self.main_region_coords,
            confidence=0.6,
            cat_dir=self.cat_dir
        )

    def execute(self):
        self.go_to_world()
        
        self.click_ri_chang()
        self.scoll_and_click(direction='down')
        self.scoll_and_click(
            direction='up', 
            other_target=self.fuben,
            other_target_name=self.fuben_name,
        )

        self.get_fu_ben_page_indicator_coords(wait_time=120, target_region='副本页面', is_to_click=False)

        multi_challenge_auth_coords = self.get_multi_challenge_auth_coords()
        if self.to_save_times:
            if multi_challenge_auth_coords is not None:
                self.open_or_close_checkbox(
                    operation='close',
                    target_region=self.fb_coords_manager.region_for_check_multi_challenge()
                )
            else:
                print("完成: 该账号没有多次挑战权限!")

        self.get_buy_times_icon_coords(target_region='购买次数图标')
        actual_buy_times = self.buy_times_in_store(self.buy_times, 'buy_times_not_enough')

        # 如果不存储次数, 那么将购买的次数加到实际挑战次数中
        if self.to_save_times is False:
            self.challenge_times += actual_buy_times

        print(f'完成: 总共挑战次数为{self.challenge_times}次!')
        self.zu_dui()
        for i in range(self.challenge_times):
            print(f'开始第{i+1}次挑战!')
            # 点击挑战, 进入副本
            tiao_zhan_coords = self.get_tiao_zhan_coords()
            click_region(tiao_zhan_coords, seconds=0)
            
            self.get_tiao_zhan_alert_coords(wait_time=2, target_region='挑战提示框', is_to_click=True, 
                                            wait_time_before_click=1, to_raise_exception=False)

            # 检查2秒内是否弹出挑战次数不足的提示框
            start_time = time.time()
            while True:
                if time.time() - start_time > 2:
                    break
                
                times_not_enough_coords = self.get_times_not_enough()
                if times_not_enough_coords is not None:
                    raise Exception("挑战次数不足, 退出挑战!")

            # 如果弹出购买次数不足提示框, 则挑战结束
            if self.get_buy_times_not_enough() is not None:
                print("完成: 挑战次数不足!")
                break
            
            self.get_tiao_zhan_over_coords(wait_time=480, target_region='挑战结束', is_to_click=True)

            # 如果是最后一次挑战, 则不需要再次进入副本
            if i == self.challenge_times - 1:
                print('完成: 所有次数已用完!')
                break
            
            # 获取进入副本的坐标点, 点击进入
            self.get_fu_ben_enter_coords(wait_time=120, target_region='进入副本', is_to_click=True)
            self.zu_dui()
            
        print('挑战结束!')

if __name__ == '__main__':
    try:
        main_region_coords = get_game_page_coords(resolution = resolution)
    except Exception as e:
        print(f"未定位到游戏界面!")

    coords_manager = FuBenCoordsManager(main_region_coords)
    main_region_coords = coords_manager.main_region_coords

    fuben_executor = FuBenExecutor(coords_manager, '广寒界', buy_times=3)

    fuben_executor.execute()


