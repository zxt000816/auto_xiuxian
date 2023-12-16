from coords_manager import *
from utils import *
import pyautogui
import time
import numpy as np
import pandas as pd
from xiuxian_exception import *

class BaseExecutor:
    def __init__(self, coords_manager: BaseCoordsManager, target: str):
        # 初始化函数，接收坐标管理器和目标参数
        self.coords_manager = coords_manager
        self.main_region_coords = self.coords_manager.main_region_coords
        self.richang_coords = self.coords_manager.ri_chang()
        self.exit_coords = self.coords_manager.exit()
        self.cat_dirs = {
            'youli': 'youli',  # 游历
            'shuangxiu': 'shuangxiu',  # 双修
            'assistant': 'assistant',  # 小助手
            'huodong_baoming': 'huodong_baoming',  # 活动报名
            'fuben': 'fuben',  # 副本,
            'xi_ling': 'xi_ling',  # 洗灵,
            'hong_bao': 'hong_bao',  # 红包,
            'hun_dun_ling_ta': 'hun_dun_ling_ta',  # 混沌灵塔,
            'tiao_zhan_xian_yuan': 'tiao_zhan_xian_yuan',  # 挑战仙缘,
            'ling_shou': 'ling_shou',  # 灵兽
            'zhui_mo_gu': 'zhui_mo_gu',  # 坠魔谷
            'bai_ye': 'bai_ye',  # 拜谒
            'xiu_lian': 'xiu_lian',  # 修炼
            'qi_xi_mo_jie': 'qi_xi_mo_jie',  # 奇袭魔界
            'game_control': 'game_control',  # 游戏控制
        }
        self.taget_name_dict = {
            'youli': '游历',
            'shuangxiu': '双修',
            'assistant': '小助手',
            'huodong_baoming': '活动报名',
            'fuben': '副本',
            'xi_ling': '洗灵',
            'hong_bao': '红包',
            'hun_dun_ling_ta': '混沌灵塔',
            'tiao_zhan_xian_yuan': '挑战仙缘',
            'ling_shou': '灵兽',
            'zhui_mo_gu': '坠魔谷',
            'bai_ye': '拜谒',
            'xiu_lian': '修炼',
            'game_control': '游戏控制',
            'qi_xi_mo_jie': '奇袭魔界',
        }
        self.target = target
        self.target_name = self.taget_name_dict[self.target]
        self.cat_dir = self.cat_dirs[self.target]

    def get_leave_coords(self):
        # 获取离开按钮的坐标
        leave_imgs = [
            {'target_region_image': 'leave2', 'main_region_coords': self.main_region_coords, 'confidence': 0.6, 'grayscale': True, 'cat_dir': 'leave'},
            # {'target_region_image': 'leave1', 'main_region_coords': self.main_region_coords, 'confidence': 0.6, 'grayscale': True, 'cat_dir': 'leave'},
            {'target_region_image': 'leave3', 'main_region_coords': self.main_region_coords, 'confidence': 0.8, 'grayscale': True, 'cat_dir': 'leave'},
        ]

        leave_coords = get_region_coords_by_multi_imgs(leave_imgs)
        return leave_coords

    def get_leave_confirm_coords(self):
        # 获取离开确认按钮的坐标
        leave_confirm_imgs = [
            {'target_region_image': 'leave_confirm1', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': True, 'cat_dir': 'leave_confirm'},
            {'target_region_image': 'leave_confirm2', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': True, 'cat_dir': 'leave_confirm'},
        ]

        leave_confirm_coords = get_region_coords_by_multi_imgs(leave_confirm_imgs)
        return leave_confirm_coords

    def get_back_arrow_coords(self):
        # 获取返回按钮的坐标
        back_arrow_imgs = [
            {'target_region_image': 'back_arrow1', 'main_region_coords': self.main_region_coords, 'confidence': 0.8, 'grayscale': True, 'cat_dir': 'back_arrow'},
            {'target_region_image': 'back_arrow2', 'main_region_coords': self.main_region_coords, 'confidence': 0.8, 'grayscale': False, 'cat_dir': 'back_arrow'},
        ]
        back_arrow_coords = get_region_coords_by_multi_imgs(back_arrow_imgs)
        return back_arrow_coords
    
    def get_world_coords(self, sub_main_coords: tuple=None):
        # 获取世界图标的坐标
        _check_region_coords = self.main_region_coords if sub_main_coords is None else sub_main_coords
        world_coords = get_region_coords(
            'world_icon',
            main_region_coords=_check_region_coords,
            confidence=0.7,
        )
        return world_coords
    
    def get_network_not_stable_coords(self):
        # 获取网络不稳定的坐标
        netword_not_stable_coords = get_region_coords(
            'network_not_stable',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
        )
        return netword_not_stable_coords

    def _check_is_in_world(self):
        # 判断是否处于世界地图界面
        check_region_coords = self.coords_manager.map_or_leave()
        big_map_imgs = [
            {'target_region_image': 'big_map1', 'main_region_coords': check_region_coords, 'confidence': 0.4, 'grayscale': True},
            {'target_region_image': 'big_map2', 'main_region_coords': check_region_coords, 'confidence': 0.4, 'grayscale': True},
        ]
        big_map_coords = get_region_coords_by_multi_imgs(big_map_imgs)
        if big_map_coords is not None:
            return True
        
        return False
        
    def click_if_coords_exist(self, coords, message, seconds=2):
        # 这个函数的作用是, 需要得到点击反馈的时候, 用这个函数. 
        # (比如: 返回世界时, 如果找到了返回世界的图标, 点击之后, 返回True, 可以用来跳出循环, 进行下一个页面的操作)
        if coords is not None:
            click_region(coords, seconds=seconds)
            print(f"完成: {message}")
            return True
        return False

    def go_to_world(self):
        print("="*25 + "进入世界地图" + "="*25)
        while not self._check_is_in_world():
            # 判断的优先级: 网络不稳定 > 返回按钮 > 离开按钮 > 世界图标 > 指定位置 > 
            # 后续需要添加条件判断点击指定位置, 画面是否发生变化, 如果没有发生变化, while会陷入死循环!!!
            print("当前是否在世界地图界面: ", False)
            netword_not_stable_coords = self.get_network_not_stable_coords()
            if netword_not_stable_coords is not None:
                click_region(self.coords_manager.confirm_button_in_network_not_statble(), seconds=3)
                print("点击确定按钮, 退出网络不稳定提示框")

            leave_coords = self.get_leave_coords()
            if self.click_if_coords_exist(leave_coords, "点击离开按钮") is True:
                # 当弹出离开提示框后, 点击确认离开按钮  
                if self.get_leave_confirm_coords() is not None:
                    click_region(self.coords_manager.confirm_button_in_leave_alert(), seconds=5)
                    print("完成: 点击确认离开按钮")

                continue

            back_arrow_coords = self.get_back_arrow_coords()
            if self.click_if_coords_exist(back_arrow_coords, "点击返回按钮") is True:
                continue

            world_coords = self.get_world_coords(self.coords_manager.region_for_check_world())
            if self.click_if_coords_exist(world_coords, "点击世界图标", seconds=5):
                continue

            click_region(self.coords_manager.exit(), seconds=3)
    
    def click_ri_chang(self):
        time.sleep(1)
        click_region(self.richang_coords, seconds=2)
        print("完成: 点击日常按钮")

    def scoll_and_click(
        self, 
        direction='down', 
        other_target=None, 
        other_target_name=None,
        confidence=0.9,
        num_of_scroll=12, 
        scroll_length=300,
        scroll_seconds=5,
        grayscale=False,
        scroll_start_point_coords=None,
        cat_dir=None,
        in_ri_chang_page=True,
        is_to_click=True,
    ):
        if other_target_name is not None:
            if other_target_name is None:
                raise Exception("other_target_name can not be None")
            
            target = other_target
            target_name = other_target_name
        else:
            target = self.target
            target_name = self.target_name

        if direction not in ['up', 'down']:
            raise Exception("direction must be 'up' or 'down'")
        
        if cat_dir is None:
            cat_dir = self.cat_dir

        target_coords = get_region_coords(
            target, 
            main_region_coords=self.main_region_coords, 
            confidence=confidence, 
            cat_dir=cat_dir,
            grayscale=grayscale,
        )
        print(f"完成: 识别一次{target_name}位置")

        if target_coords is None:
            if scroll_start_point_coords is None:
                scroll_start_point_coords = self.coords_manager.scroll_start_point()
                scroll_start_point_coords = (scroll_start_point_coords[0], scroll_start_point_coords[1])
            
            move_to_specific_coords(scroll_start_point_coords)
            print(f"完成: 未找到{target_name}位置, 将鼠标移动到指定位置")
        
        scroll_length = -1 * scroll_length if direction == 'down' else scroll_length
        scroll_length = scroll_length * self.coords_manager.y_ratio
        scroll_length = int(round(scroll_length))

        while target_coords is None and num_of_scroll > 0:
            print(f"完成: 未找到{target_name}位置, 向下滚动距离{scroll_length}")
            scroll_specific_length(scroll_length, seconds=scroll_seconds)
            
            target_coords = get_region_coords(
                target, 
                main_region_coords=self.main_region_coords, 
                confidence=confidence, 
                cat_dir=cat_dir,
                grayscale=grayscale,
            )
            num_of_scroll -= 1
        
        if target_coords is None:
            raise ScrollException(f"未找到{target_name}位置.")

        if in_ri_chang_page:
            # 计算出日常列表中的, 任务的宽度和高度
            task_height, task_width = 223, 933
            task_height = task_height * self.coords_manager.y_ratio
            task_height = int(round(task_height))
            task_width = task_width * self.coords_manager.x_ratio
            task_width = int(round(task_width))
            full_target_coords = (target_coords[0], target_coords[1], task_width, task_height)

            # 在full_target_coords中, 查看是否有`已完成`的标识
            finished_task_coords = get_region_coords(
                'finished_task',
                main_region_coords=full_target_coords,
                confidence=0.7,
            )
            if finished_task_coords is not None:
                raise FinishedTaskException(f"{target_name}任务已经完成, 无需点击")

        if is_to_click:
            click_region(target_coords, seconds=3)
            print(f"完成: 点击{target_name}按钮")

    def if_buy_store_pop_up(self):
        buy_store_coords_is_in_main_region = get_region_coords(
            'buy_store', 
            main_region_coords=self.main_region_coords, 
            confidence=0.9, 
        )
        if buy_store_coords_is_in_main_region:
            return True
        else:
            return False

    def buy_times_in_store(self, buy_times: int, buy_times_not_enough_indicator: str = None):
        print("="*25 + f"购买{self.target_name}次数" + "="*25)
        actual_buy_times = 0

        if buy_times_not_enough_indicator is not None:
            buy_times_not_enough_indicator_coords = get_region_coords(
                buy_times_not_enough_indicator,
                main_region_coords=self.main_region_coords,
                confidence=0.8,
                cat_dir=self.cat_dir,
            )
            if buy_times_not_enough_indicator_coords is not None:
                print("完成: 购买次数已用完")
                click_region(self.exit_coords, seconds=2)
                return actual_buy_times

        # 显示100灵石, 目前已购买0次; 显示150灵石, 目前已购买1次; 显示200灵石, 目前已购买2次; 显示250灵石, 目前已购买3次
        price_to_times = {100: 0, 150: 1, 200: 2, 250: 3} 
        current_lingshi_coords = self.coords_manager.current_lingshi()
        current_lingshi_image = pyautogui.screenshot(region=current_lingshi_coords)
        current_lingshi_arr = np.array(current_lingshi_image)
        current_lingshi = extract_int_from_image(current_lingshi_arr, error_value=float('-inf'))

        price_in_store_coords = self.coords_manager.price_in_store()
        price_in_store_image = pyautogui.screenshot(region=price_in_store_coords)
        price_in_store_arr = np.array(price_in_store_image)
        price = extract_int_from_image(price_in_store_arr, error_value=float('inf')) #  从图片中提取失败时, 返回float('inf')
        
        times_already_bought = price_to_times[price]
        if times_already_bought >= buy_times:
            click_region(self.exit_coords, seconds=2)
            # raise YouLiLingShiException("完成: 购买次数已用完, 将购买次数置为0")
            print("完成: 已经购买过了, 不需要购买!")
            actual_buy_times = buy_times
        else:
            buy_in_store_coords = self.coords_manager.buy_button_in_store()
            buy_times = buy_times - times_already_bought
            for _ in range(buy_times):
                if current_lingshi < price:
                    click_region(self.exit_coords, seconds=2)
                    # raise YouLiLingShiException("灵石不足, 购买失败")
                    print("灵石不足, 购买失败")
                    return actual_buy_times
                
                click_region(buy_in_store_coords)
                current_lingshi -= price
                price += 50
                buy_times -= 1
                actual_buy_times += 1
                print("完成: 购买一次游历")
            
            if self.if_buy_store_pop_up(): # 如果购买完以后购买界面还在, 说明还可以购买
                click_region(self.exit_coords)
                print("完成: 还有剩余购买次数, 但是不买了, 退出商店界面")

        return actual_buy_times

    def open_or_close_checkbox(self, operation, target_region):
        if operation not in ['open', 'close']:
            raise InvalidOperation(f"操作`{operation}`不合法!")
        
        check_box_coords = get_region_coords(
            'check_box',
            main_region_coords=target_region,
            confidence=0.9,
        ) # 如果checkbox已经被勾选, 那么check_box_state就是一个坐标, 否则就是None

        if operation == 'open':
            if check_box_coords is None:
                click_region(check_box_coords)
                print(f"完成: checkbox已经被勾选!")
            else:
                print(f"完成: 勾选checkbox!")

        if operation == 'close':
            if check_box_coords is None:
                print(f"完成: checkbox已经被取消勾选!")
            else:
                click_region(check_box_coords)
                print(f"完成: 取消勾选checkbox!")

    @wait_region
    def check_if_specifical_event(self, wait_time, target_region, is_to_click, other_region_coords, to_raise_exception):
        return get_region_coords(
            'specifical_event',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir='game_control',
        )

class BaoMingExecutor(BaseExecutor):
    def __init__(self, baoming_coords_manager: BaoMingCoordsManager):
        super().__init__(baoming_coords_manager, 'huodong_baoming')
        self.baoming_coords_manager = baoming_coords_manager

    def click_huo_dong_bao_ming(self):
        click_region(self.coords_manager.huo_dong_bao_ming(), seconds=3)
        print("完成: 点击报名按钮")
        x, y = list(self.coords_manager.scroll_start_point())[:2]
        move_to_specific_coords((x, y), seconds=1)
    
    def start_baoming(self):
        baoming_region_coords = self.baoming_coords_manager.baoming_region()
        get_baoming_coords_args = {
            'target_region_image': 'baoming',
            'main_region_coords': baoming_region_coords, 
            'confidence': 0.5, 
            'grayscale': False,
            'cat_dir': self.cat_dir
        }

        num_to_scroll = 2
        while True:
            baoming_coords = get_region_coords(**get_baoming_coords_args)
            if baoming_coords is None:
                if num_to_scroll == 0:
                    break
                num_to_scroll -= 1
                scroll_length = -300 * self.coords_manager.y_ratio
                scroll_length = int(round(scroll_length))

                scroll_specific_length(scroll_length, seconds=4)
                continue
                
            click_region(baoming_coords, seconds=2)
            print("完成: 点击报名按钮")
            click_region(self.baoming_coords_manager.baoming_lingshi(), seconds=2)
            print("完成: 完成报名按钮")
        
        print("完成: 报名")

    def execute(self):
        self.go_to_world()

        try:
            self.click_ri_chang()
            self.click_huo_dong_bao_ming()
            self.start_baoming()
        except Exception as e:
            print(e)

        self.go_to_world()

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
            confidence=0.85,
            cat_dir='assistant',
        )
        if duihuan_alert_coords is not None:
            click_region(self.assistant_coords_manager.duihuan_run_button(), seconds=2)
            print("完成: 点击兑换运行按钮")

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

    def execute(self):
        self.go_to_world()
        try:
            self.click_ri_chang()
            self.click_assistant()
        except Exception as e:
            print(e)
            self.go_to_world()
            return
        
        for task in self.task_order:
            try:
                if self.search_task_region_and_click(task) is False:
                    print(f"未找到{self.task_name_dict[task]}位置")
                    continue

                self.process_duihuan_alert()
                if self._check_is_in_assistant() is False:
                    print(f"未进入{self.task_name_dict[task]}界面")
                    click_region(self.coords_manager.exit(), seconds=3)
                    print("完成: 点击返回按钮")
            
            except Exception as e:
                print(e)

        self.go_to_world()

class YouLiExecutor(BaseExecutor):
    def __init__(
        self,
        youli_coords_manager: YouliCoordsManager,
        place_name: str='南疆',
        buy_times: int=0,
    ):
        '''
        1. 检查是否处于世界地图界面
        2. 点击日常按钮
        3. 滚动到游历位置
        4. 点击游历
        5. 如果点击游历后, 弹出购买界面, 则购买指定次数
        6. 如果点击游历后, 弹出游历地点选择界面, 则选择指定地点
        7. 点击前往游历按钮
        8. 如果点击前往游历按钮后, 弹出游历完成界面, 则点击确定按钮
        9. 如果点击前往游历按钮后, 弹出次数不足的标识, 点击指定位置返回世界地图界面
        '''

        super().__init__(youli_coords_manager, 'youli')
        self.youli_coords_manager = youli_coords_manager
        self.place_name = place_name
        self.buy_times = buy_times
        self.place_name_dict = {
            '南疆': 'nanjiang',
            '冰海': 'binghai',
        }
        self.place_name = self.place_name_dict[self.place_name]

    def if_buy_store_pop_up(self):
        buy_store_coords_is_in_main_region = get_region_coords(
            'buy_store', 
            main_region_coords=self.main_region_coords, 
            confidence=0.9, 
            cat_dir='youli'
        )
        if buy_store_coords_is_in_main_region is not None:
            return True
        else:
            return False

    def scroll_and_click_youli(self):
        self.scoll_and_click(direction='down')
        print("商店是否弹出: ", self.if_buy_store_pop_up())
        if self.if_buy_store_pop_up():
            if self.buy_times == 0:
                print("完成: 购买次数用完或者不需要购买")
            
            self.buy_youli()
            self.scoll_and_click(direction='up')

    def buy_youli(self):
        print("="*25 + "购买游历" + "="*25)
        # 显示100灵石, 目前已购买0次; 显示150灵石, 目前已购买1次; 显示200灵石, 目前已购买2次; 显示250灵石, 目前已购买3次
        price_to_times = {100: 0, 150: 1, 200: 2, 250: 3} 
        current_lingshi_coords = self.youli_coords_manager.current_lingshi()
        current_lingshi_image = pyautogui.screenshot(region=current_lingshi_coords)
        current_lingshi_arr = np.array(current_lingshi_image)
        current_lingshi = extract_int_from_image(current_lingshi_arr, error_value=float('-inf'))

        price_in_store_coords = self.youli_coords_manager.price_in_store()
        price_in_store_image = pyautogui.screenshot(region=price_in_store_coords)
        price_in_store_arr = np.array(price_in_store_image)
        price = extract_int_from_image(price_in_store_arr, error_value=float('inf')) #  从图片中提取失败时, 返回float('inf')
        
        times_already_bought = price_to_times[price]
        if times_already_bought >= self.buy_times:
            self.buy_times = 0
            click_region(self.exit_coords, seconds=2)
            raise YouLiLingShiException("完成: 购买次数已用完, 将购买次数置为0")
        else:
            buy_in_store_coords = self.youli_coords_manager.buy_button_in_store()
            buy_times = self.buy_times - times_already_bought
            for _ in range(buy_times):
                if current_lingshi < price:
                    click_region(self.exit_coords, seconds=2)
                    raise YouLiLingShiException("灵石不足, 购买失败")
                
                click_region(buy_in_store_coords)
                current_lingshi -= price
                price += 50
                self.buy_times -= 1
                print("完成: 购买一次游历")
            
            if self.if_buy_store_pop_up(): # 如果购买完以后购买界面还在, 说明还可以购买
                click_region(self.exit_coords)
                print("完成: 还有剩余购买次数, 但是不买了, 退出商店界面")

    def scroll_to_youli_place(self):
        pass

    def choose_youli_place(self):
        print("="*25 + "选择游历地点" + "="*25)
        place_coords = get_region_coords(
            self.place_name, 
            main_region_coords=self.main_region_coords, 
            confidence=0.9, 
            cat_dir='youli'
        )
        print("完成: 查看想要游历的地点是否在屏幕内")

        if place_coords is None:
            # 后续需要实现向左滑动的逻辑
            raise YouLiPlaceException("未能找到想要游历的地点, 游历失败")
            
        click_region(place_coords, seconds=2)
        print("完成: 点击想要游历的地点")

    def start_youli(self):
        print("="*25 + "开始游历" + "="*25)
        youli_end_indicator_coords = None
        while youli_end_indicator_coords is None:
            youli_start_coords = self.youli_coords_manager.youli_start()
            click_region(youli_start_coords, seconds=4)
            print("完成: 点击`前往游历`按钮")

            youli_end_indicator_coords = get_region_coords(
                'youli_end_indicator', 
                main_region_coords=self.main_region_coords, 
                confidence=0.7, 
                cat_dir='youli'
            )

            print("完成: 查看是否匹配到游历结束的界面")

            if youli_end_indicator_coords is not None:
                print("完成: 匹配到游历结束的界面")
                break
            else:
                print("完成: 未匹配到游历结束的界面")
                buy_store_coords_is_in_main_region = self.if_buy_store_pop_up()
                if buy_store_coords_is_in_main_region:
                    self.buy_youli()

                youli_end_one_time_coords = self.youli_coords_manager.youli_end_one_time()
                click_region(youli_end_one_time_coords, seconds=2)
                print("完成: 点击一次游历结束按钮")

    def execute(self):
        self.go_to_world()

        try:
            self.click_ri_chang()
            self.scroll_and_click_youli()
            self.scroll_to_youli_place()
            self.choose_youli_place()
            self.start_youli()
        except Exception as e:
            print(e)

        self.go_to_world()

class ShuangXiuExecutor(BaseExecutor):
    def __init__(
        self,
        shuangxiu_coords_manager: ShuangXiuCoordsManager,
        gongfashu_name: str
    ):
        super().__init__(shuangxiu_coords_manager, 'shuangxiu')

        self.shuangxiu_coords_manager = shuangxiu_coords_manager
        self.gongfashu_name = gongfashu_name
        self.gongfashu_name_dict = {
            '颠凤培元': 'dian_feng_pei_yuan',
            '痴情咒': 'chi_qing_zhou',
            '六欲练心': 'liu_yu_lian_xin',
            '引龙诀': 'yin_long_jue',
            '百花烟雨': 'bai_hua_yan_yu',
        }
        self.gongfashu = self.gongfashu_name_dict[self.gongfashu_name]

        # self.gonfa_order = ['dian_feng_pei_yuan', 'liu_yu_lian_xin']
        self.main_region_coords = self.shuangxiu_coords_manager.main_region_coords

    def click_shuangxiu_gongfashu(self):
        # 在日常界面中，点击双修图标
        gongfashu_coords = get_region_coords(
            self.gongfashu,
            main_region_coords=self.main_region_coords, 
            confidence=0.9, 
            cat_dir='shuangxiu'
        )
        print(f"完成: 识别一次{self.gongfashu_name}位置")

        if gongfashu_coords is None:
            raise Exception(f"未找到{self.gongfashu_name}位置")

        click_region(gongfashu_coords, seconds=3)
        print(f"完成: 点击{self.gongfashu_name}按钮")

    def confirm_yaoqing_daoyou_is_exist(self):
        for yaoqing_daoyou in ['yaoqing_daoyou1', 'yaoqing_daoyou2']:
            yaoqing_daoyou_coords = get_region_coords(
                yaoqing_daoyou, 
                main_region_coords=self.main_region_coords, 
                confidence=0.8, 
                cat_dir='shuangxiu'
            )
            if yaoqing_daoyou_coords is not None:
                return True, yaoqing_daoyou_coords
            
        return False, None

    def click_yaoqing_daoyou(self):
        # 在双修界面中，点击邀请道友按钮
        yaoqing_daoyou_is_exist, yaoqing_daoyou_coords = self.confirm_yaoqing_daoyou_is_exist()
        
        if yaoqing_daoyou_is_exist is False:
            raise Exception("未找到邀请道友按钮")
        
        click_region(yaoqing_daoyou_coords, seconds=4)
        print("完成: 点击邀请道友按钮")

    def go_to_xianyuan_page(self):
        # 前往仙缘界面
        xianyuan_page_coords = self.shuangxiu_coords_manager.xianyuan_page()
        click_region(xianyuan_page_coords, seconds=3)
        print("完成: 前往仙缘界面")

    def click_yaoqing(self):
        # 在仙缘邀请界面中，点击邀请按钮
        yaoqing_region_coords = self.shuangxiu_coords_manager.yaoqing_region()
        args = {
            'target_region_image':'yaoqing', 
            'main_region_coords': yaoqing_region_coords, 
            'confidence': 0.9, 
            'grayscale': True,
            'cat_dir': 'shuangxiu'
        }

        while get_region_coords(**args) is None:
            scroll_length = 600 * self.shuangxiu_coords_manager.y_ratio
            scroll_length = int(round(scroll_length))
            scroll_specific_length(length=scroll_length)

        yaoqing_coords = get_region_coords(**args)
        click_region(yaoqing_coords, seconds=3)
    
    def confirm_go_to_xiulian_is_exist(self):
        go_to_xiulian_coords = get_region_coords(
            'go_to_xiulian',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir='shuangxiu'
        )
        if go_to_xiulian_coords is None:
            return False
        else:
            return True

    def confirm_shuangxiu_is_over(self):
        shuangxiu_over_indicator_coords = get_region_coords(
            'shuangxiu_over_indicator',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir='shuangxiu'
        )

        if shuangxiu_over_indicator_coords is None:
            return False
        else:
            return True

    def click_go_to_xiulian(self):
        # 在双修界面中，点击前往修炼按钮
        go_to_xiulian_coords = self.shuangxiu_coords_manager.go_to_xiulian()
        click_region(go_to_xiulian_coords, seconds=4)
        print("完成: 点击前往修炼按钮")

    def speed_up_shuangxiu(self):
        # 在双修界面中，点击屏幕中心, 可以快速跳过双修动画
        while self.confirm_go_to_xiulian_is_exist() is False:
            click_region(self.shuangxiu_coords_manager.main_region_coords, seconds=2)
            print("完成: 点击屏幕中心")
        
        time.sleep(4)

    def extract_remain_times(self):
        remain_times_coords = self.shuangxiu_coords_manager.remain_times()
        remain_times_image = pyautogui.screenshot(region=remain_times_coords)
        remain_times_image_array = np.array(remain_times_image)
        remain_times = extract_int_from_image(remain_times_image_array, 3)
        self.remain_times = remain_times

    def execute(self):
        self.go_to_world()

        try:
            self.click_ri_chang()
            self.scoll_and_click(direction='down')
            # self.click_shuangxiu_gongfashu()
            self.scoll_and_click(
                direction='down', 
                other_target=self.gongfashu, 
                other_target_name=self.gongfashu_name,
                scroll_length=400,
                scroll_seconds=3
            )
            self.click_yaoqing_daoyou()
            self.go_to_xianyuan_page()
            self.click_yaoqing()
            self.extract_remain_times()

            while self.remain_times > 0:
                self.click_go_to_xiulian()
                if self.confirm_shuangxiu_is_over():
                    break

                self.speed_up_shuangxiu()
                self.remain_times -= 1
                print(f"剩余双修次数: {self.remain_times}")
                if self.remain_times > 0:
                    self.click_yaoqing_daoyou()
                    self.go_to_xianyuan_page()
                    self.click_yaoqing()
            
            print("完成: 双修结束!")

        except Exception as e:
            print(e)

        self.go_to_world()
    
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
            confidence=0.9,
            grayscale=True,
            cat_dir=self.cat_dir
        )
    
    def get_chuang_jian_dui_wu_coords(self):
        return get_region_coords(
            'chuang_jian_dui_wu',
            self.main_region_coords,
            confidence=0.9,
            grayscale=True,
            cat_dir=self.cat_dir
        )

    def get_zu_dui_alert_coords(self):
        return get_region_coords(
            'zu_dui_alert',
            self.main_region_coords,
            confidence=0.8,
            grayscale=True,
            cat_dir=self.cat_dir
        )

    def get_yao_qing_coords(self):
        return get_region_coords(
            'yao_qing',
            self.main_region_coords,
            confidence=0.8,
            grayscale=True,
            cat_dir=self.cat_dir
        )

    def get_yao_qing_fen_shen(self):
        return get_region_coords(
            'yao_qing_fen_shen',
            self.main_region_coords,
            confidence=0.8,
            grayscale=True,
            cat_dir=self.cat_dir
        )
    
    def get_team_is_full(self):
        return get_region_coords(
            'team_is_full',
            self.main_region_coords,
            confidence=0.7,
            grayscale=True,
            cat_dir=self.cat_dir
        )

    def zu_dui(self):
        self.get_zui_dui_coords(wait_time=10, target_region='组队按钮', is_to_click=True)
        
        # 如果弹出队伍列表, 则点击创建队伍
        chuang_jian_dui_wu_coords = self.get_chuang_jian_dui_wu_coords()
        if chuang_jian_dui_wu_coords is not None:
            click_region(chuang_jian_dui_wu_coords, seconds=2)
            print("完成: 点击创建队伍按钮")

        # 如果弹出队伍设置界面, 则点击确认
        time.sleep(2)
        zu_dui_alert_coords = self.get_zu_dui_alert_coords()
        if zu_dui_alert_coords is not None:
            click_region(self.fb_coords_manager.zu_dui_alert_confirm(), seconds=2)
            while True:
                yao_qing_coords = self.get_yao_qing_coords()
                if not yao_qing_coords:
                    break
                
                click_region(yao_qing_coords, seconds=2)
                click_region(self.fb_coords_manager.fen_shen_page(), seconds=2)
                click_region(self.get_yao_qing_fen_shen(), seconds=2)
                
                if self.get_team_is_full():
                    # 队伍人满时, 会弹出提示框, 点击退出坐标点
                    click_region(self.fb_coords_manager.exit(), seconds=2)
                
                # 完成一次邀请后, 点击退出坐标点
                click_region(self.fb_coords_manager.exit(), seconds=2)
            
            # 退出邀请页面, 回到副本界面
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
        fu_ben_page_indicator_coords = get_region_coords(
            'fu_ben_page_indicator',
            self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir
        )
        return fu_ben_page_indicator_coords
    
    def get_wu_ci_shu_alert(self):
        return get_region_coords(
            'wu_ci_shu_alert',
            self.main_region_coords,
            confidence=0.6,
            cat_dir=self.cat_dir
        )

    def execute(self):
        self.go_to_world()
        try:
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
                
                # 检查2秒内是否弹出挑战次数不足的提示框
                start_time = time.time()
                while True:
                    if time.time() - start_time > 2:
                        break
                    
                    wu_ci_shu_alert_coords = self.get_wu_ci_shu_alert()
                    if wu_ci_shu_alert_coords is not None:
                        raise Exception("挑战次数不足, 退出挑战!")

                # 如果弹出购买次数不足提示框, 则挑战结束
                if self.get_buy_times_not_enough() is not None:
                    print("完成: 挑战次数不足!")
                    break
                
                self.get_tiao_zhan_over_coords(wait_time=120, target_region='挑战结束', is_to_click=True)

                # 如果是最后一次挑战, 则不需要再次进入副本
                if i == self.challenge_times - 1:
                    print('完成: 所有次数已用完!')
                    break
                
                # 获取进入副本的坐标点, 点击进入
                self.get_fu_ben_enter_coords(wait_time=120, target_region='进入副本', is_to_click=True)
                self.zu_dui()
                
            print('挑战结束!')

        except Exception as e:
            print(e)

        self.go_to_world()

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
        ling_shi_hong_bao_coords = get_region_coords(
            'ling_shi_hong_bao',
            main_region_coords=self.hong_bao_coords_manager.main_region_coords,
            confidence=0.8,
            cat_dir='hong_bao',
        )
        return ling_shi_hong_bao_coords

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
        click_region(self.hong_bao_coords_manager.chat())

        # 滚动到包含红包的对话
        while True:
            try:
                self.scoll_and_click(direction='down', other_target='hong_bao', other_target_name='红包', num_of_scroll=3)

                hong_bao_coords = self.get_hon_bao_coords()
                if not self.click_if_coords_exist(hong_bao_coords, message='检测到红包'):
                    raise Exception('没有检测到红包，可能已经领完了')
                
                ling_shi_hong_bao_coords = self.get_ling_shi_hong_bao_coords()
                click_region(ling_shi_hong_bao_coords)
                
                self.start_ling_qu_hong_bao()
                # 点击指定返回坐标点两次, 返回到对话列表界面
                click_region(self.hong_bao_coords_manager.exit(), seconds=2)
                click_region(self.hong_bao_coords_manager.exit(), seconds=2)
            
            except Exception as e:
                print(e)
                break

        self.go_to_world()

class HunDunLingTaExecutor(BaseExecutor):
    def __init__(self, hun_dun_ling_ta_coords_manager: HunDunLingTaCoordsManager, ling_ta_name: str):
        super().__init__(hun_dun_ling_ta_coords_manager, 'hun_dun_ling_ta')
        self.hun_dun_ling_ta_coords_manager = hun_dun_ling_ta_coords_manager
        self.ling_ta_name_dict = {
            '弥罗之塔': 'mi_luo_zhi_ta',
            '天月之塔': 'tian_yue_zhi_ta',
            '摩诃之塔': 'mo_he_zhi_ta',
        }
        self.ling_ta = self.ling_ta_name_dict[ling_ta_name]

    @wait_region
    def get_open_indicator_coords(self, wait_time, target_region):
        ling_ta_open_indicator_coords = get_region_coords(
            'open_indicator',
            main_region_coords=self.hun_dun_ling_ta_coords_manager.main_region_coords,
            confidence=0.8,
            cat_dir='hun_dun_ling_ta',
        )
        return ling_ta_open_indicator_coords
    
    @wait_region
    def get_sweep_coords(self, wait_time, target_region):
        sweep_coords = get_region_coords(
            'sweep',
            main_region_coords=self.hun_dun_ling_ta_coords_manager.main_region_coords,
            confidence=0.8,
            cat_dir='hun_dun_ling_ta',
        )
        return sweep_coords
    
    @wait_region
    def get_start_sweep_coords(self, wait_time, target_region):
        start_sweep_coords = get_region_coords(
            'start_sweep',
            main_region_coords=self.hun_dun_ling_ta_coords_manager.main_region_coords,
            confidence=0.8,
            cat_dir='hun_dun_ling_ta',
        )
        return start_sweep_coords
    
    def get_sweep_over_coords(self):
        sweep_over_coords = get_region_coords(
            'sweep_over',
            main_region_coords=self.hun_dun_ling_ta_coords_manager.main_region_coords,
            confidence=0.8,
            cat_dir='hun_dun_ling_ta',
        )
        return sweep_over_coords

    def execute(self):
        self.go_to_world()
        
        try:
            self.click_ri_chang()
            self.scoll_and_click(direction='down')

            # 确认`混沌灵塔`是否打开
            self.get_open_indicator_coords(wait_time=120, target_region='混沌灵塔')

            # 点击混沌灵塔界面的扫荡按钮
            sweep_coords = self.get_sweep_coords(wait_time=10, target_region='扫荡')
            click_region(sweep_coords)

            # 如果弹出扫荡完成界面, 则返回世界
            sweep_over_coords = self.get_sweep_over_coords()
            if sweep_over_coords is None:
                # 如果没有弹出扫荡完成界面, 则点击开始扫荡
                start_sweep_coords = self.get_start_sweep_coords(wait_time=10, target_region='开始扫荡')
                click_region(start_sweep_coords)
        
        except Exception as e:
            print(e)
            
        self.go_to_world()

class TiaoZhanXianYuanExecutor(BaseExecutor):
    def __init__(self, tzxy_coords_manager: TiaoZhanXianYuanCoordsManager, xian_yuan_role_name: str):
        super().__init__(tzxy_coords_manager, 'tiao_zhan_xian_yuan')
        self.tzxy_coords_manager = tzxy_coords_manager
        self.role_name_dict = {
            '尸魈': 'shi_xiao',
            '乌丑': 'wu_chou',
            '王婵': 'wang_chan',
            '势不两立': 'shi_bu_liang_li'
        }
        self.xian_yuan_role_name = xian_yuan_role_name
        self.xian_yuan_role = self.role_name_dict[xian_yuan_role_name]

    @wait_region
    def get_open_tiao_zhan_xian_yuan_coords(self, wait_time, target_region, is_to_click=False):
        tiao_zhan_xian_yuan_coords = get_region_coords(
            'open_tiao_zhan_xian_yuan',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir
        )
        return tiao_zhan_xian_yuan_coords
    
    @wait_region
    def get_jiao_ta_zuo_ren_coords(self, wait_time, target_region, is_to_click=False):
        jiao_ta_zuo_ren_coords = get_region_coords(
            'jiao_ta_zuo_ren',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
        return jiao_ta_zuo_ren_coords

    @wait_region
    def get_kan_zhao_ba_coords(self, wait_time, target_region, is_to_click=False):
        kan_zhao_ba_coords = get_region_coords(
            'kan_zhao_ba',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir,
        )
        return kan_zhao_ba_coords
    
    @wait_region
    def get_battle_over_coords(self, wait_time, target_region, is_to_click=False):
        battle_over_coords = get_region_coords(
            'battle_over',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
        return battle_over_coords
    
    @wait_region
    def get_battle_over2_coords(self, wait_time, target_region, is_to_click=False):
        battle_over2_coords = get_region_coords(
            'battle_over2',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            grayscale=True,
            cat_dir=self.cat_dir,
        )
        return battle_over2_coords

    def execute(self):
        self.go_to_world()
        
        try:
            self.click_ri_chang()
            self.scoll_and_click(direction='down')

            # 确认`仙缘页面`是否打开
            self.get_open_tiao_zhan_xian_yuan_coords(wait_time=3, target_region='仙缘页面', is_to_click=False)
            click_region(self.tzxy_coords_manager.all_xian_yuan())
                    
            self.scoll_and_click(
                direction='down', 
                other_target=self.xian_yuan_role, 
                other_target_name=self.xian_yuan_role_name, 
                confidence=0.7,
                num_of_scroll=20,
                scroll_length=400, 
                scroll_seconds=4
            )
            click_region(self.tzxy_coords_manager.qian_wang())

            # 确认`教他做人`是否出现
            self.get_jiao_ta_zuo_ren_coords(wait_time=120, target_region='教他做人',is_to_click=True)

            # 确认`看招吧`是否出现
            self.get_kan_zhao_ba_coords(wait_time=10, target_region='看招吧', is_to_click=True)

            # 确认`战斗结束`是否出现
            self.get_battle_over_coords(wait_time=60, target_region='战斗结束', is_to_click=True)

            # 确认`战斗结束2`是否出现
            self.get_battle_over2_coords(wait_time=20, target_region='战斗结束2', is_to_click=False)
            click_region(self.tzxy_coords_manager.exit())

        except Exception as e:
            print(e)

        self.go_to_world()

class LingShouExecutor(BaseExecutor):
    def __init__(self, ls_coords_manager: LingShouCoordsManager, buy_times: int, to_save_times: bool = True):
        super().__init__(ls_coords_manager, 'ling_shou')
        self.ls_coords_manager = ls_coords_manager
        self.buy_times = buy_times
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
            confidence=0.8,
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
        buy_times_not_enough_indicator_coords = get_region_coords(
            'buy_times_not_enough_indicator',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir
        )
        return buy_times_not_enough_indicator_coords

    def execute(self):
        self.go_to_world()
        
        try:
            self.click_ri_chang()
            self.scoll_and_click(direction='down')

            self.get_open_ling_shou_coords(wait_time=120, target_region='灵兽界面', is_to_click=False)
            self.get_tui_jian_coords(wait_time=10, target_region='推荐剿灭', is_to_click=True)

            # 如果要存储次数, 那么就要关掉多人挑战, 否则就打开
            multi_challenge_auth_coords = self.get_multi_challenge_auth_coords()
            if self.to_save_times:
                if multi_challenge_auth_coords is not None:
                    self.open_or_close_checkbox(
                        operation='close', 
                        target_region=self.ls_coords_manager.region_for_check_mutli_challenge()
                    )
                else:
                    print("完成: 该账号没有多人挑战的权限!")

            self.get_buy_times_icon_coords(target_region='购买次数图标')
            actual_buy_times = self.buy_times_in_store(self.buy_times, 'buy_times_not_enough_indicator')

            # 如果不存储次数, 那么将购买的次数加到挑战次数上
            if self.to_save_times is False:
                self.challenge_times = self.challenge_times + actual_buy_times

            print(f"完成: 总共挑战次数为{self.challenge_times}次!")
            for i in range(self.challenge_times):
                print(f"完成: 开始第{i + 1}次剿灭!")
                self.get_qian_wang_jiao_mie_coords(wait_time=10, target_region='前往剿灭', is_to_click=True)
                if self.get_buy_times_not_enough_indicator_coords() is not None:
                    print("完成: 挑战次数不足!")
                    break

                self.get_jiao_mie_over_coords(wait_time=120, target_region='剿灭结束', is_to_click=True)

                if i == self.challenge_times - 1:
                    print("完成: 所有次数已用完!")
                    break

                self.get_ling_shou_fu_ben_enter_coords(wait_time=120, target_region='灵兽副本进入', is_to_click=True)
                self.get_open_ling_shou_coords(wait_time=120, target_region='灵兽界面', is_to_click=False)
                self.get_tui_jian_coords(wait_time=10, target_region='推荐剿灭', is_to_click=True)
        
        except Exception as e:
            print(e)

        self.go_to_world()

class BaiYeExecutor(BaseExecutor):
    def __init__(self, by_coords_manager: BaiYeCoordsManager, event_name: str, fa_ze_level=1):
        super().__init__(by_coords_manager, 'bai_ye')
        if event_name not in ['兽渊', '魔道', '云梦', '虚天殿', '天地奕局']:
            raise Exception('活动名字错误!')
        
        self.by_coords_manager = by_coords_manager
        self.event_name = event_name
        self.event_name_dict = {
            '兽渊': 'shou_yuan',
            '魔道': 'mo_dao',
            '云梦': 'yun_meng',
            '虚天殿': 'huan_xu',
            '天地奕局': 'xian_yi',
        }
        self.event = self.event_name_dict[self.event_name]
        self.fa_ze_level = fa_ze_level

    @drag_region
    def get_event_coords(self, wait_time, target_region, is_to_click, drag_from_coords, drag_to_coords):
        event_imgs = [
            {'target_region_image': f'{self.event}1', 'main_region_coords': self.main_region_coords, 'confidence': 0.8, 'cat_dir': self.cat_dir},
            {'target_region_image': f'{self.event}2', 'main_region_coords': self.main_region_coords, 'confidence': 0.8, 'cat_dir': self.cat_dir},
        ]
        event_coords = get_region_coords_by_multi_imgs(event_imgs)
        return event_coords
    
    @wait_region
    def get_bai_ye_start_coords(self, wait_time, target_region, is_to_click):
        bai_ye_start_coords = get_region_coords(
            'bai_ye_start',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
        return bai_ye_start_coords
    
    def get_bai_ye_over_coords(self):
        bai_ye_over_coords = get_region_coords(
            'bai_ye_over',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
        return bai_ye_over_coords

    def execute(self):
        self.go_to_world()
        try:
            self.click_ri_chang()
            self.scoll_and_click(direction='down')
            self.scoll_and_click(
                direction='down',
                other_target=f'{self.fa_ze_level}_kua_fa_ze',
                other_target_name=f'{self.fa_ze_level}跨法则',
                confidence=0.8,
                grayscale=False,
            )

            self.get_event_coords(
                wait_time=120, 
                target_region=self.event_name, 
                is_to_click=True, 
                drag_from_coords=self.by_coords_manager.drag_from(), 
                drag_to_coords=self.by_coords_manager.drag_to()
            )

            bai_ye_over_coords = self.get_bai_ye_over_coords()
            if bai_ye_over_coords:
                raise BaiYeOverException('已拜谒!')
            
            self.get_bai_ye_start_coords(wait_time=10, target_region='开始拜谒', is_to_click=True)

            bai_ye_over_coords = self.get_bai_ye_over_coords()
            if bai_ye_over_coords:
                raise BaiYeOverException('已拜谒!')
        
        except Exception as e:
            print(e)

        self.go_to_world()

class ZhuiMoGuExecutor(BaseExecutor):
    def __init__(self, zmg_coords_manager: ZhuiMoGuCoordsManager, profession_name: str, max_level='炼虚-后期-五层'):
        super().__init__(zmg_coords_manager, 'zhui_mo_gu')
        self.zmg_coords_manager = zmg_coords_manager
        self.profession_name = profession_name
        self.boss_info: pd.DataFrame = pd.read_excel('boss_info.xlsx')
        
        self.max_level_1, self.max_level_2, self.max_level_3 = max_level.split('-')
        self.level_1_numbering = { '练气': 1, '筑基': 2, '结丹': 3, '元婴': 4, '化神': 5, '炼虚': 6 }
        self.level_2_numbering = { '前期': 1, '中期': 2, '后期': 3 }
        self.level_3_numbering = { '一层': 0, '二层': 1, '三层': 2, '四层': 3, '五层': 4, '六层': 5, '七层': 6, '八层': 7, '九层': 8, '十层': 9 }
        self.max_level_numbering = self.level_1_numbering[self.max_level_1] * 100 + self.level_2_numbering[self.max_level_2] * 10 + self.level_3_numbering[self.max_level_3]

        self.profession_boss_info: pd.DataFrame = self.boss_info[(self.boss_info['职业'].str.contains(profession_name)) & (self.boss_info['等级编码'] <= self.max_level_numbering)]

    @wait_region
    def scroll_to_end_indicator_coords(self, wait_time, target_region, is_to_click):
        scroll_end_indicator_coords = get_region_coords(
            'scroll_end_indicator',
            main_region_coords=self.main_region_coords,
            confidence=0.9,
            cat_dir=self.cat_dir,
        )

        move_to_specific_coords(self.zmg_coords_manager.shou_ling_scroll_start_point()[:2], seconds=1)
        scroll_specific_length(-1000, seconds=3)

        return scroll_end_indicator_coords
    
    @wait_region
    def scroll_to_any_available_coords(self, wait_time, target_region, is_to_click):
        any_available_imgs = [
            {'target_region_image': 'indicator1', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': 'zhui_mo_gu'},
            {'target_region_image': 'indicator2', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': 'zhui_mo_gu'},
            {'target_region_image': 'indicator3', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': 'zhui_mo_gu'},
            {'target_region_image': 'indicator4', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': 'zhui_mo_gu'},
            {'target_region_image': 'indicator5', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': 'zhui_mo_gu'},
            {'target_region_image': 'indicator6', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': 'zhui_mo_gu'},
            {'target_region_image': 'indicator7', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': 'zhui_mo_gu'},
            {'target_region_image': 'indicator8', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': 'zhui_mo_gu'},
        ]
        any_available_coords = get_region_coords_by_multi_imgs(any_available_imgs)
        if any_available_coords is None:
            move_to_specific_coords(self.zmg_coords_manager.shou_ling_scroll_start_point()[:2], seconds=1)
            scroll_specific_length(500, seconds=3)
        
        return any_available_coords
    
    def determine_order_of_current_boss(self):
        # 进入副本页面和, 根据首领名称, 确定当前首领的顺序
        for i, row in self.boss_info.iterrows():
            _boss = row['英文名']
            _boss_coords = get_region_coords(
                _boss,
                main_region_coords=self.main_region_coords,
                confidence=0.7,
                cat_dir=self.cat_dir,
            )
            if _boss_coords is not None:
                print(f"当前首领为: {row['首领名称']}")
                return row['等级编码']
            
        raise Exception('没有检测到当前首领是哪个!')
    
    @wait_region
    def get_qian_wang_tiao_zhan_coords(self, wait_time, target_region, is_to_click):
        qian_wang_tiao_zhan_coords = get_region_coords(
            'qian_wang_tiao_zhan',
            main_region_coords=self.main_region_coords,
            confidence=0.9,
            cat_dir=self.cat_dir,
        )
        return qian_wang_tiao_zhan_coords

    @search_region    
    def search_boss(self, boss, wait_time, target_region, region_to_click, region_to_click_name):
        boss_coords = get_region_coords(
            boss,
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir,
        )
        return boss_coords
    
    @wait_region_not_raise_exception
    def get_shou_ling_leng_que_coords(self, wait_time, target_region, is_to_click):
        shou_ling_leng_que_coords = get_region_coords(
            'shou_ling_leng_que',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir,
        )
        return shou_ling_leng_que_coords
    
    @wait_region_not_raise_exception
    def get_ci_shu_not_enough_coords(self, wait_time, target_region, is_to_click):
        ci_shu_not_enough_coords = get_region_coords(
            'ci_shu_not_enough',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir,
        )
        return ci_shu_not_enough_coords
    
    @wait_region
    def get_shou_ling_icon_coords(self, wait_time, target_region, is_to_click):
        shou_ling_icon_coords = get_region_coords(
            'shou_ling_icon',
            main_region_coords=self.main_region_coords,
            confidence=0.6,
            cat_dir=self.cat_dir,
        )
        return shou_ling_icon_coords

    def go_to_shou_ling_page(self, boss, boss_name, method):
        if method not in ['日常图标', '首领图标']:
            raise ValueError(f"method参数错误, 应为`日常图标`或`首领图标`")
        
        if method == '日常图标':
            self.click_ri_chang()
            self.scoll_and_click(direction='down')
        else:
            # 检查是否有首领图标, 如果有, 点击首领图标, 没有则报错
            self.get_shou_ling_icon_coords(wait_time=120, target_region='首领图标', is_to_click=True)

        # 滚动到首领列表底端, 然后点击最后一个首领打开首领页面     
        # self.scroll_to_end_indicator_coords(wait_time=60, target_region='炼虚后期-霜晶云凤', is_to_click=True)
        self.scroll_to_any_available_coords(wait_time=60, target_region='任何可以进入副本的区域', is_to_click=True)

        # 判断当前是哪个首领, 获取该首领的等级编码
        current_boss_order = self.determine_order_of_current_boss()
        print(f"当前首领的等级编码为: {current_boss_order}")
        
        # 获取目标首领的等级编码,根据等级编码, 确定点击左箭头还是右箭头
        target_boss_order = self.boss_info[self.boss_info['英文名'] == boss]['等级编码'].item()
        print(f"目标首领的等级编码为: {target_boss_order}")

        if target_boss_order == current_boss_order:
            print(f"当前首领为目标首领, 不需要切换首领!")
            return
        elif target_boss_order > current_boss_order:
            to_click_region = self.zmg_coords_manager.right_arrow()
        else:
            to_click_region = self.zmg_coords_manager.left_arrow()

        self.search_boss(boss, wait_time=60, target_region=boss_name, region_to_click=to_click_region, region_to_click_name='左箭头')

    def check_boss_state(self, boss, boss_name, method='首领图标'):
        self.go_to_shou_ling_page(boss, boss_name, method)
        # 如果匹配到当前正在挑战的首领, 则停留在当前页面, 直到观察到首领冷却, 代表首领挑战结束
        shou_ling_leng_que_coords = self.get_shou_ling_leng_que_coords(wait_time=360, target_region='首领冷却', is_to_click=False)
        if shou_ling_leng_que_coords is not None:
            print(f"首领被击败, 等待冷却中...")
            return True
        else:
            print(f"首领未被击败, 重新挑战...")
            return False

    def execute(self):
        self.go_to_world()

        try:
            for i, row in self.profession_boss_info.iterrows():
                boss_name = row['首领名称']
                boss = row['英文名']

                self.go_to_shou_ling_page(boss, boss_name, method='日常图标')

                shou_ling_leng_que_coords = self.get_shou_ling_leng_que_coords(wait_time=2, target_region='首领冷却', is_to_click=False)
                if shou_ling_leng_que_coords is not None:
                    print(f"首领冷却中，跳过{boss_name}")
                    self.go_to_world()
                    continue

                self.get_qian_wang_tiao_zhan_coords(wait_time=2, target_region='前往挑战', is_to_click=True)
                ci_shu_not_enough_coords = self.get_ci_shu_not_enough_coords(wait_time=2, target_region='次数不足', is_to_click=False)
                if ci_shu_not_enough_coords is not None:
                    click_region(self.zmg_coords_manager.exit())
                    raise CiShuNotEnoughException(f"次数不足，结束坠魔谷挑战!")
                
                boss_state = self.check_boss_state(boss, boss_name, method='首领图标')
                if boss_state:
                    print(f"首领被击败, 寻找下一个首领...")
                    self.go_to_world()
                    continue
                else:
                    raise BossNotDefeatedException(f"首领未被击败, 重新挑战...")

        except Exception as e:
            print(e)

        self.go_to_world()

class GameControlExecutor(BaseExecutor):
    def __init__(self, cc_coords_manager: GameControlCoordsManager, account_name: str, account: str):
        super().__init__(cc_coords_manager, 'game_control')
        self.cc_coords_manager = cc_coords_manager
        self.account_name = account_name
        self.account = account

    @wait_region
    def get_menu_expansion_coords(self, wait_time, target_region, is_to_click, click_wait_time):
        menu_expansion_imgs = [
            {'target_region_image': 'menu_expansion1', 'main_region_coords': self.main_region_coords, 'confidence': 0.6, 'grayscale': True, 'cat_dir': 'game_control'},
            {'target_region_image': 'menu_expansion2', 'main_region_coords': self.main_region_coords, 'confidence': 0.6, 'grayscale': True, 'cat_dir': 'game_control'},
            {'target_region_image': 'menu_expansion3', 'main_region_coords': self.main_region_coords, 'confidence': 0.6, 'grayscale': True, 'cat_dir': 'game_control'},
        ]
        return get_region_coords_by_multi_imgs(menu_expansion_imgs)
    
    @wait_region
    def get_setting_coords(self, wait_time, target_region, is_to_click, click_wait_time):
        return get_region_coords(
            'setting',
            self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir
        )
    
    @wait_region
    def get_exit_login_coords(self, wait_time, target_region, is_to_click, click_wait_time):
        return get_region_coords(
            'exit_login',
            self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir
        )
    
    @wait_region
    def get_exit_login_alert_coords(self, wait_time, target_region, is_to_click, click_wait_time, other_region_coords):
        return get_region_coords(
            'exit_login_alert',
            self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir
        )
    
    @wait_region
    def get_login_button_coords(self, wait_time, target_region, is_to_click, click_wait_time, other_region_coords):
        return get_region_coords(
            'login_button',
            self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir
        )

    def scroll_to_top(self, scroll_start_point_coords, scroll_length, scroll_seconds, scroll_times=5):
        pyautogui.moveTo(scroll_start_point_coords)
        for _ in range(scroll_times):
            scroll_specific_length(scroll_length, scroll_seconds)

    @wait_region
    def get_login_successfully_coords(self, wait_time, target_region, is_to_click, other_region_coords):
        return get_region_coords(
            'login_successfully',
            self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir
        )
    
    @wait_region
    def get_start_game_coords(self, wait_time, target_region, is_to_click):
        return get_region_coords(
            'start_game',
            self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir
        )
    
    @wait_region
    def get_start_game_successfully_coords(self, wait_time, target_region):
        start_game_successfully_imgs = [
            {'target_region_image': 'start_game_successfully1', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': 'game_control'},
            {'target_region_image': 'start_game_successfully2', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': 'game_control'},
            {'target_region_image': 'start_game_successfully3', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': 'game_control'},
            {'target_region_image': 'start_game_successfully4', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': 'game_control'},
            {'target_region_image': 'start_game_successfully5', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': 'game_control'},
            {'target_region_image': 'start_game_successfully6', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': 'game_control'},
        ]
        return get_region_coords_by_multi_imgs(start_game_successfully_imgs)

    @wait_region
    def get_vip_fu_li_coords(self, wait_time, target_region, is_to_click, other_region_coords, to_raise_exception):
        return get_region_coords(
            'vip_fu_li',
            self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir
        )
    
    @wait_region
    def get_restart_game_coords(self, wait_time, target_region, is_to_click, other_region_coords, to_raise_exception):
        return get_region_coords(
            'restart_game',
            self.main_region_coords,
            confidence=0.7,
            cat_dir=self.cat_dir
        )
    
    def exit_current_account(self):
        self.go_to_world()
        # 点击展开菜单
        click_region(self.cc_coords_manager.menu_expansion(), seconds=1)
        # 点击设置
        self.get_setting_coords(wait_time=5, target_region="设置", is_to_click=True, click_wait_time=1)
        # 点击退出登录
        self.get_exit_login_coords(wait_time=5, target_region="退出登录", is_to_click=True, click_wait_time=1)
        # 确认是否弹出退出登录确认框, 如果弹出, 则点击确认
        self.get_exit_login_alert_coords(
            wait_time=5, target_region="退出登录确认框", is_to_click=True, click_wait_time=1, 
            other_region_coords=self.cc_coords_manager.confirm_in_exit_login_alert()
        )

    def execute(self, restart_game=False):
        if restart_game is False:
            
            self.exit_current_account()

            # 如果检测到登录按钮, 则点击账户区域
            self.get_login_button_coords(
                wait_time=5, target_region="登录按钮", is_to_click=True, click_wait_time=1, 
                other_region_coords=self.cc_coords_manager.account_region()
            )
            # 滚动到顶部
            self.scroll_to_top(
                scroll_start_point_coords=self.cc_coords_manager.scroll_account_ls()[:2],
                scroll_length=1000,
                scroll_seconds=1,
            )
            # 滚动账户列表, 点击指定账户
            self.scoll_and_click(
                direction='down',
                other_target=self.account,
                other_target_name=self.account_name,
                confidence=0.7,
                cat_dir='users',
                scroll_length=300,
                scroll_seconds=3,
                scroll_start_point_coords=self.cc_coords_manager.scroll_account_ls()[:2],
                is_to_click=True,
                in_ri_chang_page=False,
            )

            # 点击登录按钮
            self.get_login_button_coords(
                wait_time=5, target_region="登录按钮", is_to_click=True, click_wait_time=1,
                other_region_coords=None 
            )

        # 判断是否弹出vip福利, 如果弹出, 则点击关闭
        self.get_vip_fu_li_coords(
            wait_time=3, target_region="vip福利", is_to_click=True, 
            other_region_coords=self.cc_coords_manager.close_vip_fu_li(), to_raise_exception=False
        )

        # 等待登录成功
        self.get_login_successfully_coords(
            wait_time=15, target_region="登录成功", is_to_click=True, 
            other_region_coords=self.cc_coords_manager.exit()
        )

        # 点击开始游戏
        self.get_start_game_coords(wait_time=15, target_region="开始游戏", is_to_click=True)

        restart_game_coords = self.get_restart_game_coords(
            wait_time=2, target_region="重新开始游戏", is_to_click=True, 
            other_region_coords=self.cc_coords_manager.confirm_button_in_restart_game(), to_raise_exception=False
        )
        if restart_game_coords is not None:
            # 如果弹出重新开始游戏, 则点击确认, 然后重新执行
            print("等待游戏重新开始...")
            time.sleep(60)
            return self.execute(restart_game=True)

        self.check_if_specifical_event(
            wait_time=5,
            target_region="是否弹出特殊活动",
            is_to_click=True,
            other_region_coords=self.cc_coords_manager.close_specifical_event(),
            to_raise_exception=False
        )

        # 等待开始游戏成功
        self.get_start_game_successfully_coords(wait_time=30, target_region="开始游戏成功")

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

    def execute(self):
        self.go_to_world()
        try:
            self.click_ri_chang()
            self.scoll_and_click(direction='down')

            self.get_last_qi_xi_alert(
                wait_time=3,
                target_region='上次奇袭魔界提示框',
                is_to_click=True,
                other_region_coords=self.qxmj_coords_manager.confirm_button_in_last_qi_xi_alert(),
                to_raise_exception=False,
            )

            self.get_can_yu_jin_gong(
                wait_time=5,
                target_region='参与进攻',
                is_to_click=True,
                other_region_coords=None,
                to_raise_exception=True,
            )

            self.get_kun_nan(
                wait_time=3,
                target_region='困难',
                is_to_click=True,
                other_region_coords=None,
                to_raise_exception=True,
            )

            self.get_chuang_jian_dui_wu_coords(
                wait_time=3,
                target_region='创建队伍',
                is_to_click=True,
                other_region_coords=None,
                to_raise_exception=True,
            )

            self.get_chuang_jian_dui_wu_alert(
                wait_time=3,
                target_region='创建队伍提示框',
                is_to_click=True,
                other_region_coords=self.qxmj_coords_manager.confirm_button_in_chuang_jian_dui_wu(),
                to_raise_exception=True,
            )

        except Exception as e:
            print(e)

        self.go_to_world()
