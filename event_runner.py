from coords_manager import *
from utils import get_region_coords, click_region, extract_int_from_image,\
                  move_to_specific_coords, scroll_specific_length, get_region_coords_by_multi_imgs
import pyautogui
import time
import numpy as np
from xiuxian_exception import *

class BaseExecutor:
    def __init__(self, coords_manager: BaseCoordsManager, target: str):
        self.coords_manager = coords_manager
        self.main_region_coords = self.coords_manager.main_region_coords
        self.richang_coords = self.coords_manager.ri_chang()
        self.exit_coords = self.coords_manager.exit()
        self.cat_dirs = {
            'youli': 'youli',
            'shuangxiu': 'shuangxiu',
            'assistant': 'assistant',
            'huodong_baoming': 'huodong_baoming',
        }
        self.taget_name_dict = {
            'youli': '游历',
            'shuangxiu': '双修',
            'assistant': '小助手',
            'huodong_baoming': '活动报名',
        }
        self.target = target
        self.target_name = self.taget_name_dict[self.target]
        self.cat_dir = self.cat_dirs[self.target]

    def get_leave_coords(self):
        leave_imgs = [
            {'target_region_image': 'leave2', 'main_region_coords': self.main_region_coords, 'confidence': 0.6, 'grayscale': True, 'cat_dir': 'leave'},
            {'target_region_image': 'leave1', 'main_region_coords': self.main_region_coords, 'confidence': 0.6, 'grayscale': True, 'cat_dir': 'leave'},
            {'target_region_image': 'leave3', 'main_region_coords': self.main_region_coords, 'confidence': 0.8, 'grayscale': True, 'cat_dir': 'leave'},
        ]

        leave_coords = get_region_coords_by_multi_imgs(leave_imgs)
        return leave_coords

    def get_leave_confirm_coords(self):
        leave_confirm_imgs = [
            {'target_region_image': 'leave_confirm1', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': True, 'cat_dir': 'leave_confirm'},
            {'target_region_image': 'leave_confirm2', 'main_region_coords': self.main_region_coords, 'confidence': 0.7, 'grayscale': True, 'cat_dir': 'leave_confirm'},
        ]

        leave_confirm_coords = get_region_coords_by_multi_imgs(leave_confirm_imgs)
        return leave_confirm_coords

    def get_back_arrow_coords(self):
        back_arrow_imgs = [
            {'target_region_image': 'back_arrow1', 'main_region_coords': self.main_region_coords, 'confidence': 0.6, 'grayscale': True, 'cat_dir': 'back_arrow'},
            {'target_region_image': 'back_arrow2', 'main_region_coords': self.main_region_coords, 'confidence': 0.6, 'grayscale': False, 'cat_dir': 'back_arrow'},
        ]
        back_arrow_coords = get_region_coords_by_multi_imgs(back_arrow_imgs)
        return back_arrow_coords
    
    def get_world_coords(self, sub_main_coords: tuple=None):
        _check_region_coords = self.main_region_coords if sub_main_coords is None else sub_main_coords
        world_coords = get_region_coords(
            'world_icon',
            main_region_coords=_check_region_coords,
            confidence=0.7,
        )
        return world_coords

    def _check_is_in_world(self):
        check_region_coords = self.coords_manager.map_or_leave()
        big_map_coords = None
        for image_name in ['big_map', 'big_map2']:
            big_map_coords = get_region_coords(
                image_name,
                main_region_coords=check_region_coords,
                confidence=0.4,
                grayscale=True,
            )
            if big_map_coords is not None:
                return True
        
        return False
        
    def click_if_coords_exist(self, coords, message):
        # 这个函数的作用是, 需要得到点击反馈的时候, 用这个函数. 
        # (比如: 返回世界时, 如果找到了返回世界的图标, 点击之后, 返回True, 可以用来跳出循环, 进行下一个页面的操作)
        if coords is not None:
            click_region(coords, seconds=3)
            print(f"完成: {message}")
            return True
        return False

    def go_to_world(self):
        print("="*25 + "进入世界地图" + "="*25)
        while not self._check_is_in_world():
            # 判断的优先级: 返回按钮 > 离开按钮 > 世界图标 > 指定位置
            # 后续需要添加条件判断点击指定位置, 画面是否发生变化, 如果没有发生变化, while会陷入死循环!!!
            print("当前是否在世界地图界面: ", False)
            leave_coords = self.get_leave_coords()
            if self.click_if_coords_exist(leave_coords, "点击离开按钮") is True:
                # 当弹出离开提示框后, 点击确认离开按钮  
                if self.get_leave_confirm_coords() is not None:
                    click_region(self.coords_manager.confirm_button_in_leave_alert(), seconds=3)
                    print("完成: 点击确认离开按钮")

                continue

            back_arrow_coords = self.get_back_arrow_coords()
            if self.click_if_coords_exist(back_arrow_coords, "点击返回按钮") is True:
                continue

            world_coords = self.get_world_coords(self.coords_manager.region_for_check_world())
            if self.click_if_coords_exist(world_coords, "点击世界图标"):
                continue
            
            click_region(self.coords_manager.exit(), seconds=3)
    
    def click_ri_chang(self):
        click_region(self.richang_coords, seconds=3)
        print("完成: 点击日常按钮")

    def scoll_and_click(self, direction='down'):
        if direction not in ['up', 'down']:
            raise Exception("direction must be 'up' or 'down'")
        
        target_coords = get_region_coords(
            self.target, 
            main_region_coords=self.main_region_coords, 
            confidence=0.9, 
            cat_dir=self.cat_dir
        )
        print(f"完成: 识别一次{self.target_name}位置")

        num_of_scroll = 6
        if target_coords is None:
            scoll_start_point_coords = self.coords_manager.scroll_start_point()
            scoll_start_point_coords = (scoll_start_point_coords[0], scoll_start_point_coords[1])
            move_to_specific_coords(scoll_start_point_coords)
            print(f"完成: 未找到{self.target_name}位置, 将鼠标移动到指定位置")
        
        while target_coords is None and num_of_scroll > 0:
            print(f"完成: 未找到{self.target_name}位置, 向下滚动一次")
            scroll_length = -600 if direction == 'down' else 600
            scroll_length = scroll_length * self.coords_manager.y_ratio
            scroll_length = int(round(scroll_length))
            print(f"完成: 滚动距离{scroll_length}")
            print(f"滚动方向: {direction}")
            scroll_specific_length(scroll_length, seconds=5)
            
            target_coords = get_region_coords(
                self.target, 
                main_region_coords=self.main_region_coords, 
                confidence=0.9, 
                cat_dir=self.cat_dir
            )
            num_of_scroll -= 1
        
        if target_coords is None:
            raise ScrollException(f"未找到{self.target_name}位置.")

        self.target_coords = target_coords
        click_region(target_coords, seconds=3)
        print(f"完成: 点击{self.target_name}按钮")

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
                scroll_length = 600 * self.coords_manager.y_ratio
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
        self.click_ri_chang()
        self.click_huo_dong_bao_ming()
        self.start_baoming()
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
            raise Exception(f"未找到{task_name}图标")

        self.search_run_button_and_click(task_image_coords)

    def execute(self):
        self.go_to_world()
        self.click_ri_chang()
        self.click_assistant()
        for task in self.task_order:
            self.search_task_region_and_click(task)
            self.process_duihuan_alert()
            if self._check_is_in_assistant() is False:
                print(f"未进入{self.task_name_dict[task]}界面")
                click_region(self.coords_manager.exit(), seconds=3)
                print("完成: 点击返回按钮")
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
                confidence=0.9, 
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
            if self._check_is_in_world() is False:
                raise Exception("当前不在世界地图界面")
            self.click_ri_chang()
            self.scroll_and_click_youli()
            self.scroll_to_youli_place()
            self.choose_youli_place()
            self.start_youli()
        except (ScrollException, YouLiPlaceException, YouLiLingShiException) as e:
            print(e)
        except Exception as e:
            print(e)

        self.go_to_world()
