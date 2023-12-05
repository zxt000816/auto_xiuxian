import pyautogui
import numpy as np
from typing import Tuple
from utils import *
from coords_manager import AssistantCoordsManager, BaoMingCoordsManager, YouliCoordsManager, ShuangXiuCoordsManager, BaseCoordsManager
from event_runner import AssistantExecutor, BaoMingExecutor, YouLiExecutor, ShuangXiuExecutor, BaseExecutor

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True
resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)

try:
    main_region_coords = get_game_page_coords(resolution = resolution)
except Exception as e:
    print(f"未定位到游戏界面!")

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

class FuBenExecutor(BaseExecutor):
    def __init__(
        self, 
        coords_manager: FuBenCoordsManager, 
        fuben_name: str,
        buy_times=3
    ):
        super().__init__(coords_manager, 'fuben')
        self.coords_manager = coords_manager
        self.fuben_name = fuben_name
        self.buy_times = buy_times
        self.fuben_name_dict = {
            '昆吾山': 'kun_wu_shan',
            '天澜圣殿': 'tian_lan_sheng_dian',
            '深海巢穴': 'shen_hai_chao_xue',
            '越国皇宫': 'yue_guo_huang_gong',
            '血色禁地': 'xue_se_jin_di',
        }
        self.fuben = self.fuben_name_dict[fuben_name]
        self.finish_buying_times = False

    def get_tiao_zhan_coords(self):
        return get_region_coords(
            'tiao_zhan',
            self.coords_manager.main_region_coords,
            confidence=0.9,
            grayscale=True,
            cat_dir=self.cat_dir
        )
    
    def get_chuang_jian_dui_wu_coords(self):
        return get_region_coords(
            'chuang_jian_dui_wu',
            self.coords_manager.main_region_coords,
            confidence=0.9,
            grayscale=True,
            cat_dir=self.cat_dir
        )

    def get_zu_dui_alert_coords(self):
        return get_region_coords(
            'zu_dui_alert',
            self.coords_manager.main_region_coords,
            confidence=0.8,
            grayscale=True,
            cat_dir=self.cat_dir
        )

    def get_yao_qing_coords(self):
        return get_region_coords(
            'yao_qing',
            self.coords_manager.main_region_coords,
            confidence=0.8,
            grayscale=True,
            cat_dir=self.cat_dir
        )

    def get_yao_qing_fen_shen(self):
        return get_region_coords(
            'yao_qing_fen_shen',
            self.coords_manager.main_region_coords,
            confidence=0.8,
            grayscale=True,
            cat_dir=self.cat_dir
        )
    
    def get_team_is_full(self):
        return get_region_coords(
            'team_is_full',
            self.coords_manager.main_region_coords,
            confidence=0.7,
            grayscale=True,
            cat_dir=self.cat_dir
        )

    def zu_dui(self):
        zu_dui_coords = get_region_coords(
            'zu_dui',
            self.coords_manager.main_region_coords,
            confidence=0.9,
            cat_dir=self.cat_dir
        )

        if self.click_if_coords_exist(zu_dui_coords, message='点击组队按钮', seconds=3):
            # 如果弹出队伍列表, 则点击创建队伍
            chuang_jian_dui_wu_coords = self.get_chuang_jian_dui_wu_coords()
            if chuang_jian_dui_wu_coords:
                click_region(chuang_jian_dui_wu_coords, seconds=2)

            # 如果弹出队伍设置界面, 则点击确认
            zu_dui_alert_coords = self.get_zu_dui_alert_coords()
            if zu_dui_alert_coords:
                click_region(self.coords_manager.zu_dui_alert_confirm(), seconds=2)
                while True:
                    yao_qing_coords = self.get_yao_qing_coords()
                    if not yao_qing_coords:
                        break
                    
                    click_region(yao_qing_coords, seconds=2)
                    click_region(self.coords_manager.fen_shen_page(), seconds=2)
                    click_region(self.get_yao_qing_fen_shen(), seconds=2)
                    
                    if self.get_team_is_full():
                        # 队伍人满时, 会弹出提示框, 点击退出坐标点
                        click_region(self.coords_manager.exit(), seconds=2)
                    
                    # 完成一次邀请后, 点击退出坐标点
                    click_region(self.coords_manager.exit(), seconds=2)
                
                # 退出邀请页面, 回到副本界面
                click_region(self.coords_manager.exit(), seconds=2)
        else:
            raise Exception('未找到组队按钮!')

    def get_buy_times_not_enough(self):
        return get_region_coords(
            'buy_times_not_enough',
            self.coords_manager.main_region_coords,
            confidence=0.8,
            grayscale=True,
            cat_dir=self.cat_dir
        )
    
    def get_buy_store(self):
        return get_region_coords(
            'buy_store',
            self.coords_manager.main_region_coords,
            confidence=0.7,
            grayscale=True,
            cat_dir=self.cat_dir
        )

    def buy_fu_ben_times(self):
        print('已经在副本界面!')
        click_region(self.coords_manager.buy_times_button(), seconds=2)
        self.buy_times_in_store(self.buy_times, 'buy_times_not_enough')
        self.finish_buying_times = True

    def get_tiao_zhan_multiple_times(self):
        return get_region_coords(
            'tiao_zhan_multiple_times',
            self.coords_manager.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir
        )
    
    # 确定副本实际挑战的次数
    def get_real_fuben_times(self):
        if self.get_tiao_zhan_multiple_times():
            return 1
        
        real_tiao_zhan_times_coords = self.coords_manager.real_tiao_zhan_times()
        real_tiao_zhan_times_image = pyautogui.screenshot(region=real_tiao_zhan_times_coords)
        real_tiao_zhan_times_array = np.array(real_tiao_zhan_times_image)
        real_tiao_zhan_times = extract_int_from_image(real_tiao_zhan_times_array, 3)
        return real_tiao_zhan_times

    def get_fu_ben_go_in_coords(self):
        return get_region_coords(
            f'{self.fuben}_go_in',
            self.coords_manager.main_region_coords,
            confidence=0.7,
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
        ### 这段代码需要改善 ###
        time.sleep(5) # 可能会赶往副本界面, 需要等待
        while self.finish_buying_times == False:
            self.buy_fu_ben_times()
        ### 这段代码需要改善 ###
        
        real_tiao_zhan_times = self.get_real_fuben_times()
        print(f'实际挑战次数: {real_tiao_zhan_times}')
        self.zu_dui()

        for i in range(real_tiao_zhan_times):
            print(f'开始第{i+1}次挑战!')
            # 每次挑战都需要重新拉分身
            if i != 0:
                self.zu_dui()

            # 点击挑战, 进入副本
            tiao_zhan_coords = self.get_tiao_zhan_coords()
            click_region(tiao_zhan_coords, seconds=2)
            
            # 如果弹出购买次数不足提示框, 则挑战结束
            if self.get_buy_times_not_enough():
                break

            # 首先等待40秒, 然后每隔3秒检查是否在世界
            time.sleep(40)
            while True:
                if self._check_is_in_world():
                    break
                else:
                    time.sleep(3)

            # 如果是最后一次挑战, 则不需要再次进入副本
            if i == real_tiao_zhan_times - 1:
                break
            
            # 获取进入副本的坐标点, 点击进入
            fu_ben_go_in_coords = self.get_fu_ben_go_in_coords()
            click_region(fu_ben_go_in_coords, seconds=3)
        
        print('挑战结束!')

        self.go_to_world()

coords_manager = FuBenCoordsManager(main_region_coords)
main_region_coords = coords_manager.main_region_coords

fuben_executor = FuBenExecutor(coords_manager, '昆吾山', buy_times=2)
fuben_executor.execute()