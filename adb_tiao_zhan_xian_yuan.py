import pyautogui
import time
import numpy as np
from utils_adb import get_region_coords_by_multi_imgs, get_region_coords, get_game_page_coords, extract_int_from_image
from coords_manager import BaseCoordsManager
from event_executor import BaseExecutor
from xiuxian_exception import *
from typing import Tuple
import adbutils

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True

adb = adbutils.AdbClient(host="127.0.0.1", port=5037)

global device
global main_region_coords

device = adb.device(serial="emulator-5560")
main_region_coords = get_game_page_coords()

def scroll_specific_length(
    start_x: float,
    end_x: float,
    start_y: float,
    end_y: float,
    seconds: int = 3, 
    # main_region_coords: Tuple[int, int, int, int] = (0, 0, 1080, 1920)
):
    # minus length means scroll down
    # plus length means scroll up

    print(main_region_coords)
    
    width = main_region_coords[2]
    height = main_region_coords[3]

    start_x = start_x * width
    start_x = int(round(start_x))

    end_x = end_x * width
    end_x = int(round(end_x))

    start_y = start_y * height
    start_y = int(round(start_y))

    end_y = end_y * height
    end_y = int(round(end_y))

    print(f"swipe: ({start_x}, {start_y}) -> ({end_x}, {end_y})")
    device.swipe(start_x, start_y, end_x, end_y, duration=1.5)
    time.sleep(seconds)

def click_region(
    region_coords, 
    button='left', 
    seconds=2, 
    # main_region_coords=(0, 0, 1080, 1920)
):
    x, y = pyautogui.center(region_coords)
    x = x - main_region_coords[0]
    y = y - main_region_coords[1]
    device.click(x, y)
    time.sleep(seconds)

def wait_region(func):
    def wrapper(self, *args, **kwargs):
        start_time = time.time()
        wait_time = kwargs.get('wait_time', 3)
        target_region = kwargs.get('target_region', None)
        is_to_click = kwargs.get('is_to_click', False)
        click_wait_time = kwargs.get('click_wait_time', 2)
        other_region_coords = kwargs.get('other_region_coords', None)
        to_raise_exception = kwargs.get('to_raise_exception', True)
        wait_time_before_click = kwargs.get('wait_time_before_click', 0)
        print(f"完成: 等待{wait_time}秒, 等待`{target_region}`出现...")
        while True:
            if time.time() - start_time > wait_time:
                if to_raise_exception:
                    raise TargetRegionNotFoundException(f"完成: 等待超时, `{target_region}`未出现!")
                else:
                    print(f"完成: 等待超时, `{target_region}`未出现!")
                    return None
            
            result_coords = func(self, *args, **kwargs)
            if result_coords:
                print(f"完成: `{target_region}`出现!")
                if is_to_click:
                    if other_region_coords:
                        time.sleep(wait_time_before_click)
                        click_region(other_region_coords, seconds=click_wait_time)
                    else:
                        time.sleep(wait_time_before_click)
                        click_region(result_coords, seconds=click_wait_time)
                        print(f"完成: 点击{target_region}!")
                    
                return result_coords

    return wrapper

def wait_region(func):
    def wrapper(self, *args, **kwargs):
        start_time = time.time()
        device = kwargs.get('device', None)
        wait_time = kwargs.get('wait_time', 3)
        target_region = kwargs.get('target_region', None)
        is_to_click = kwargs.get('is_to_click', False)
        click_wait_time = kwargs.get('click_wait_time', 2)
        other_region_coords = kwargs.get('other_region_coords', None)
        to_raise_exception = kwargs.get('to_raise_exception', True)
        wait_time_before_click = kwargs.get('wait_time_before_click', 0)
        print(f"完成: 等待{wait_time}秒, 等待`{target_region}`出现...")
        while True:
            if time.time() - start_time > wait_time:
                if to_raise_exception:
                    raise TargetRegionNotFoundException(f"完成: 等待超时, `{target_region}`未出现!")
                else:
                    print(f"完成: 等待超时, `{target_region}`未出现!")
                    return None
            
            result_coords = func(self, *args, **kwargs)
            if result_coords:
                print(f"完成: `{target_region}`出现!")
                if is_to_click:
                    if other_region_coords:
                        time.sleep(wait_time_before_click)
                        click_region(other_region_coords, seconds=click_wait_time)
                    else:
                        time.sleep(wait_time_before_click)
                        click_region(result_coords, seconds=click_wait_time)
                        print(f"完成: 点击{target_region}!")
                    
                return result_coords

    return wrapper

class BaseExecutor:
    def __init__(self, coords_manager: BaseCoordsManager, target: str = None):
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
            'lun_dao': 'lun_dao',  # 论道
            'bai_zu_gong_feng': 'bai_zu_gong_feng',  # 百族供奉
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
            'lun_dao': '论道',
            'bai_zu_gong_feng': '百族供奉',
        }
        self.target = target
        self.target_name = self.taget_name_dict.get(self.target, None)
        self.cat_dir = self.cat_dirs.get(self.target, None)

    @wait_region
    def get_general_coords(self, wait_time, target_region, is_to_click, to_raise_exception, device):
        return get_region_coords(
            'general',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            grayscale=False
        )
    
    @wait_region
    def get_gong_fa_shu_icon_coords(self, wait_time, target_region, is_to_click, click_wait_time, to_raise_exception):
        # 获取返回按钮的坐标
        back_arrow_imgs = [
            {'target_region_image': 'gong_fa_shu_icon1', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': None},
            {'target_region_image': 'gong_fa_shu_icon2', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': None},
        ]
        back_arrow_coords = get_region_coords_by_multi_imgs(back_arrow_imgs)
        return back_arrow_coords

    def get_leave_coords(self):
        # 获取离开按钮的坐标
        leave_imgs = [
            {'target_region_image': 'leave2', 'main_region_coords': self.main_region_coords, 'confidence': 0.6, 'grayscale': True, 'cat_dir': 'leave'},
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
        network_not_stable_coords = get_region_coords(
            'network_not_stable',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
        )
        return network_not_stable_coords
    
    @wait_region
    def get_chao_li_fan_li_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'chao_zhi_fan_li',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            grayscale=False
        )
    
    @wait_region
    def get_close_chao_zhi_fan_li_coords(self, wait_time, target_region, is_to_click, wait_time_before_click, to_raise_exception):
        return get_region_coords(
            'close_chao_zhi_fan_li',
            main_region_coords=self.main_region_coords,
            confidence=0.7,
            grayscale=False
        )
    
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

            network_not_stable_coords = self.get_network_not_stable_coords()
            if network_not_stable_coords is not None:
                click_region(self.coords_manager.confirm_button_in_network_not_statble(), seconds=3)
                print("点击确定按钮, 退出网络不稳定提示框")

            chao_zhi_fan_li_coords = self.get_chao_li_fan_li_coords(wait_time=2, target_region='超值返利', is_to_click=False, to_raise_exception=False)
            if chao_zhi_fan_li_coords is not None:
                self.get_close_chao_zhi_fan_li_coords(wait_time=2, target_region='关闭超值返利', is_to_click=True, 
                                                      wait_time_before_click=1, to_raise_exception=False)

            click_region(self.coords_manager.exit(), seconds=3)
    
    def calculate_scroll_length(self, length: int):
        # 计算滚动的长度
        scroll_length = length * self.coords_manager.y_ratio
        scroll_length = int(round(scroll_length))
        return scroll_length

    def click_ri_chang(self):
        time.sleep(1)
        click_region(self.richang_coords, seconds=2)
        print("完成: 点击日常按钮")

    def scroll_and_click(
        self, 
        direction='down', 
        other_target=None, 
        other_target_name=None,
        confidence=0.8,
        num_of_scroll=12, 
        scroll_length=300,
        scroll_seconds=3,
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
            
            # move_to_specific_coords(scroll_start_point_coords)
            print(f"完成: 未找到{target_name}位置, 将鼠标移动到指定位置")
        
        scroll_length = -1 * scroll_length if direction == 'down' else scroll_length
        scroll_length = self.calculate_scroll_length(scroll_length)

        while target_coords is None and num_of_scroll > 0:
            print(f"完成: 未找到{target_name}位置, 向下滚动距离{scroll_length}")
            # scroll_specific_length(scroll_length, seconds=scroll_seconds)
            scroll_specific_length(
                start_x=0.5,
                end_x=0.5,
                start_y=0.66,
                end_y=0.33,
                seconds=scroll_seconds,
            )
            
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
                confidence=0.8,
            )
            if finished_task_coords is not None:
                raise FinishedTaskException(f"{target_name}任务已经完成, 无需点击")

        if is_to_click:
            click_region(target_coords, seconds=3)
            print(f"完成: 点击{target_name}按钮")

    def scroll_and_click_by_multiple_imgs(
        self, 
        direction, 
        targets_imgs_info, 
        target_name,
        num_of_scroll=12, 
        scroll_length=300,
        scroll_seconds=3,
        in_ri_chang_page=True,
        is_to_click=True,
    ):
        if direction not in ['up', 'down']:
            raise Exception("direction must be 'up' or 'down'")
        
        target_coords = get_region_coords_by_multi_imgs(targets_imgs_info)
        print(f"完成: 识别一次{target_name}位置")

        if target_coords is None:
            scroll_start_point_coords = self.coords_manager.scroll_start_point()
            scroll_start_point_coords = (scroll_start_point_coords[0], scroll_start_point_coords[1])
            
            # move_to_specific_coords(scroll_start_point_coords)
            print(f"完成: 未找到{target_name}位置, 将鼠标移动到指定位置")
        
        scroll_length = -1 * scroll_length if direction == 'down' else scroll_length
        scroll_length = self.calculate_scroll_length(scroll_length)

        while target_coords is None and num_of_scroll > 0:
            print(f"完成: 未找到{target_name}位置, 向下滚动距离{scroll_length}")
            # scroll_specific_length(scroll_length, seconds=scroll_seconds)
            scroll_specific_length(
                start_x=0.5,
                end_x=0.5,
                start_y=0.66,
                end_y=0.33,
                seconds=scroll_seconds,
            )
            
            target_coords = get_region_coords_by_multi_imgs(targets_imgs_info)
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
                confidence=0.8,
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

    def buy_times_in_store(
        self, 
        buy_times: int, 
        buy_times_not_enough_indicator: str = None, 
        to_raise_exception=False,
        price_in_store_coords=None,
        price_to_times: dict = None,
    ):
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
        if price_to_times is None:
            price_to_times = {100: 0, 150: 1, 200: 2, 250: 3} 
            
        current_lingshi_coords = self.coords_manager.current_lingshi()
        current_lingshi_image = pyautogui.screenshot(region=current_lingshi_coords)
        current_lingshi_arr = np.array(current_lingshi_image)
        current_lingshi = extract_int_from_image(current_lingshi_arr, error_value=0)

        if price_in_store_coords is None:
            price_in_store_coords = self.coords_manager.price_in_store()

        price_in_store_image = pyautogui.screenshot(region=price_in_store_coords)
        price_in_store_arr = np.array(price_in_store_image)
        price = extract_int_from_image(price_in_store_arr, error_value=250) #  从图片中提取失败时, 返回float('inf')
        
        times_already_bought = price_to_times.get(price) # 已经购买的次数(如果price是100, 那么times_already_bought就是0)
        if times_already_bought >= buy_times:
            click_region(self.exit_coords, seconds=2)
            actual_buy_times = buy_times
            if to_raise_exception is True:
                raise ValueError(f"完成: 购买次数已用完, 将购买次数置为0")
            else:
                print("完成: 已经购买过了, 不需要购买!")
        else:
            buy_in_store_coords = self.coords_manager.buy_button_in_store()
            buy_times = buy_times - times_already_bought
            for _ in range(buy_times):
                if current_lingshi < price:
                    click_region(self.exit_coords, seconds=2)
                    if to_raise_exception is True:
                        raise ValueError("灵石不足, 购买失败")
                    else:
                        print("灵石不足, 购买失败")
                        return actual_buy_times
                
                click_region(buy_in_store_coords)
                current_lingshi -= price
                price += 50
                buy_times -= 1
                actual_buy_times += 1
                print("完成: 购买一次")
            
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

class TiaoZhanXianYuanCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)

    def all_xian_yuan(self):
        diff=(324, 280, 160, 80)
        return self.calculate_relative_coords(diff)
    
    def qian_wang(self):
        diff=(430, 1527, 255, 96)
        return self.calculate_relative_coords(diff)

class TiaoZhanXianYuanExecutor(BaseExecutor):
    def __init__(self, tzxy_coords_manager: TiaoZhanXianYuanCoordsManager, xian_yuan_role_name: str, wei_mian: str='人界'):
        super().__init__(tzxy_coords_manager, 'tiao_zhan_xian_yuan')
        self.tzxy_coords_manager = tzxy_coords_manager
        self.role_name_dict = {
            '尸魈': 'shi_xiao',
            '乌丑': 'wu_chou',
            '王婵': 'wang_chan',
            '极阴': 'ji_yin',
            '青背苍狼': 'qing_bei_cang_lang',
            '炫烨王': 'xuan_ye_wang',
            '黄枫灵鲲': 'huang_feng_ling_kun',
            '势不两立': 'shi_bu_liang_li'
        }
        self.candidate_role_names = ['势不两立', '尸魈', '炫烨王', '极阴', '王婵', '乌丑', '青背苍狼', '黄枫灵鲲']
        self.candidate_role_names.remove(xian_yuan_role_name)
        self.xian_yuan_role_name = xian_yuan_role_name
        self.xian_yuan_role = self.role_name_dict[xian_yuan_role_name]
        self.wei_mian = wei_mian

    @wait_region
    def get_tzxy_icon_coords(self, wait_time, target_region, is_to_click, click_wait_time, to_raise_exception):
        tzxy_icon_imgs = [
            {'target_region_image': 'tzxy_icon1', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': self.cat_dir},
            {'target_region_image': 'tzxy_icon2', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': False, 'cat_dir': self.cat_dir},
        ]
        return get_region_coords_by_multi_imgs(tzxy_icon_imgs)

    @wait_region
    def get_open_tiao_zhan_xian_yuan_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
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
    def get_battle_over_coords(self, wait_time, target_region, is_to_click, wait_time_before_click):
        battle_over_coords = get_region_coords(
            'battle_over',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
        return battle_over_coords
    
    @wait_region
    def get_battle_over2_coords(self, wait_time, target_region, is_to_click, other_region_coords, wait_time_before_click):
        battle_over2_coords = get_region_coords(
            'battle_over2',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            grayscale=True,
            cat_dir=self.cat_dir,
        )
        return battle_over2_coords
    
    @wait_region
    def get_ling_jie_coords(self, wait_time, target_region, is_to_click, wait_time_before_click, to_raise_exception):
        return get_region_coords(
            'ling_jie',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
    
    @wait_region
    def get_ren_jie_coords(self, wait_time, target_region, is_to_click, wait_time_before_click, to_raise_exception):
        return get_region_coords(
            'ren_jie',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )

    def execute(self, index=0):
        self.go_to_world()
        
        # self.click_ri_chang()
        # self.scroll_and_click(direction='down')

        click_region(self.tzxy_coords_manager.menu_arrow())

        self.get_tzxy_icon_coords(wait_time=3, target_region='挑战仙缘图标', is_to_click=True, click_wait_time=3, to_raise_exception=True)

        # 确认`仙缘页面`是否打开
        self.get_open_tiao_zhan_xian_yuan_coords(wait_time=3, target_region='仙缘页面', is_to_click=False, to_raise_exception=True)
        
        if self.wei_mian == '人界':
            ren_jie_coords = self.get_ren_jie_coords(
                wait_time=3, target_region='人界', is_to_click=True, wait_time_before_click=1, to_raise_exception=False
            )
            if ren_jie_coords is None:
                click_region(self.tzxy_coords_manager.all_xian_yuan())      

        elif self.wei_mian == '灵界':
            self.get_ling_jie_coords(wait_time=3, target_region='灵界', is_to_click=True, wait_time_before_click=1, to_raise_exception=False)

        else:
            raise ValueError(f"未知的位面: {self.wei_mian}!")

        try:
            self.scroll_and_click(
                direction='down', 
                other_target=self.xian_yuan_role, 
                other_target_name=self.xian_yuan_role_name, 
                confidence=0.8,
                num_of_scroll=10,
                scroll_length=400, 
                scroll_seconds=4
            )
        except Exception as e:
            print(f"没有{self.xian_yuan_role_name}!")
            self.xian_yuan_role_name = self.candidate_role_names[index]
            self.xian_yuan_role = self.role_name_dict[self.xian_yuan_role_name]
            print(f"切换为{self.xian_yuan_role_name}!")
            self.execute(index=index+1)
            
        click_region(self.tzxy_coords_manager.qian_wang())

        # 确认`教他做人`是否出现
        self.get_jiao_ta_zuo_ren_coords(wait_time=120, target_region='教他做人',is_to_click=True)

        # 确认`看招吧`是否出现
        self.get_kan_zhao_ba_coords(wait_time=10, target_region='看招吧', is_to_click=True)

        # 确认`战斗结束`是否出现
        self.get_battle_over_coords(wait_time=60, target_region='战斗结束', is_to_click=True, wait_time_before_click=5)

if __name__ == '__main__':

    resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)

    # main_region_coords = get_game_page_coords(resolution = resolution)
    # main_region_coords = (0, 0, 1080, 1920)

    tzxy_coords_manager = TiaoZhanXianYuanCoordsManager(main_region_coords)
    executor = TiaoZhanXianYuanExecutor(tzxy_coords_manager, xian_yuan_role_name='势不两立', wei_mian='人界')
    executor.execute()
