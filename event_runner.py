from coords_manager import *
from utils import get_region_coords, click_region, extract_int_from_image,\
                  move_to_specific_coords, scroll_specific_length, get_region_coords_by_multi_imgs
import pyautogui
import time
import numpy as np
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
            'hong_bao': 'hong_bao',  # 红包
        
        }
        self.taget_name_dict = {
            'youli': '游历',
            'shuangxiu': '双修',
            'assistant': '小助手',
            'huodong_baoming': '活动报名',
            'fuben': '副本',
            'xi_ling': '洗灵',
            'hong_bao': '红包',
        }
        self.target = target
        self.target_name = self.taget_name_dict[self.target]
        self.cat_dir = self.cat_dirs[self.target]

    def get_leave_coords(self):
        # 获取离开按钮的坐标
        leave_imgs = [
            {'target_region_image': 'leave2', 'main_region_coords': self.main_region_coords, 'confidence': 0.6, 'grayscale': True, 'cat_dir': 'leave'},
            {'target_region_image': 'leave1', 'main_region_coords': self.main_region_coords, 'confidence': 0.6, 'grayscale': True, 'cat_dir': 'leave'},
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
        
    def click_if_coords_exist(self, coords, message, seconds=3):
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

    def scoll_and_click(self, direction='down', other_target=None, other_target_name=None, num_of_scroll=12):
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
        
        target_coords = get_region_coords(
            target, 
            main_region_coords=self.main_region_coords, 
            confidence=0.9, 
            cat_dir=self.cat_dir
        )
        print(f"完成: 识别一次{target_name}位置")

        if target_coords is None:
            scoll_start_point_coords = self.coords_manager.scroll_start_point()
            scoll_start_point_coords = (scoll_start_point_coords[0], scoll_start_point_coords[1])
            move_to_specific_coords(scoll_start_point_coords)
            print(f"完成: 未找到{target_name}位置, 将鼠标移动到指定位置")
        
        while target_coords is None and num_of_scroll > 0:
            print(f"完成: 未找到{target_name}位置, 向下滚动一次")
            scroll_length = -300 if direction == 'down' else 300
            scroll_length = scroll_length * self.coords_manager.y_ratio
            scroll_length = int(round(scroll_length))
            print(f"完成: 滚动距离{scroll_length}, 滚动方向: {direction}")
            scroll_specific_length(scroll_length, seconds=5)
            
            target_coords = get_region_coords(
                target, 
                main_region_coords=self.main_region_coords, 
                confidence=0.9, 
                cat_dir=self.cat_dir
            )
            num_of_scroll -= 1
        
        if target_coords is None:
            raise ScrollException(f"未找到{target_name}位置.")

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

    def buy_times_in_store(self, buy_times: int, buy_times_not_enough_indicator: str):
        print("="*25 + f"购买{self.target_name}次数" + "="*25)
        buy_times_not_enough_indicator_coords = get_region_coords(
            buy_times_not_enough_indicator,
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir,
        )
        if buy_times_not_enough_indicator_coords is not None:
            print("完成: 购买次数已用完")
            click_region(self.exit_coords, seconds=2)
            return

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
            print("完成: 购买次数已用完, 将购买次数置为0")
            return
        else:
            buy_in_store_coords = self.coords_manager.buy_button_in_store()
            buy_times = buy_times - times_already_bought
            for _ in range(buy_times):
                if current_lingshi < price:
                    click_region(self.exit_coords, seconds=2)
                    # raise YouLiLingShiException("灵石不足, 购买失败")
                    print("灵石不足, 购买失败")
                    return 
                
                click_region(buy_in_store_coords)
                current_lingshi -= price
                price += 50
                buy_times -= 1
                print("完成: 购买一次游历")
            
            if self.if_buy_store_pop_up(): # 如果购买完以后购买界面还在, 说明还可以购买
                click_region(self.exit_coords)
                print("完成: 还有剩余购买次数, 但是不买了, 退出商店界面")

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

class ShuangXiuExecutor(BaseExecutor):
    def __init__(
        self,
        shuangxiu_coords_manager: ShuangXiuCoordsManager,
        gongfashu_name: str
    ):
        super().__init__(shuangxiu_coords_manager, 'shuangxiu')

        self.shuangxiu_coords_manager = shuangxiu_coords_manager
        self.gongfashu_name = gongfashu_name
        self.shuangxiu_name_dict = {
            '颠凤培元': 'dian_feng_pei_yuan',
            '痴情咒': 'chi_qing_zhou',
            '六欲练心': 'liu_yu_lian_xin',
            '引龙诀': 'yin_long_jue',
        }
        self.gonfashu = self.shuangxiu_name_dict[self.gongfashu_name]

        self.gonfa_order = ['dian_feng_pei_yuan', 'liu_yu_lian_xin']
        self.main_region_coords = self.shuangxiu_coords_manager.main_region_coords

    def click_shuangxiu_gongfashu(self):
        # 在日常界面中，点击双修图标
        gongfashu_coords = get_region_coords(
            self.gonfashu,
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
            self.click_shuangxiu_gongfashu()
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