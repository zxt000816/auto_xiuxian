class BaseCoordsManager:
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        self.main_region_coords = main_region_coords
        self.x = main_region_coords[0]
        self.y = main_region_coords[1]
        self.width = main_region_coords[2]
        self.height = main_region_coords[3]
        self.resolution = resolution
        self.x_ratio = self.resolution[0] / 1080
        self.y_ratio = self.resolution[1] / 1920
    
    def calculate_relative_coords(self, diff, specific_region_coords=None):
        if specific_region_coords is None:
            left_top_x = self.x + diff[0] * self.x_ratio
            left_top_y = self.y + diff[1] * self.y_ratio
            width = diff[2] * self.x_ratio
            height = diff[3] * self.y_ratio
        else:
            left_top_x = specific_region_coords[0] + diff[0] * self.x_ratio
            left_top_y = specific_region_coords[1] + diff[1] * self.y_ratio
            width = diff[2] * self.x_ratio
            height = diff[3] * self.y_ratio
        
        left_top_x = round(left_top_x)
        left_top_y = round(left_top_y)
        width = round(width)
        height = round(height)

        return (left_top_x, left_top_y, width, height)
    
    # def world(self): # 修炼界面-世界地图图标
    #     diff = (30, 1695, 250, 214)
    #     return self.calculate_relative_coords(diff)
    
    def map_or_leave(self): # 在世界地图界面是`大地图`, 不在世界地图界面是`离开`
        diff = (919, 847, 148, 182)
        return self.calculate_relative_coords(diff)
    
    def region_for_check_world(self): # 修炼界面-检查世界地图图标是否存在的区域
        diff = (9, 1656, 293, 241)
        return self.calculate_relative_coords(diff)
    
    def exit(self): # 通用退出坐标点
        diff = (332, 1844, 0, 0)
        return self.calculate_relative_coords(diff)
    
    def confirm_button_in_leave_alert(self): # 离开提示框-确认按钮
        diff = (584, 1224, 302, 99)
        return self.calculate_relative_coords(diff)

    def ling_shi(self): # 世界地图界面-灵石
        diff = (842, 34, 139, 44)
        return self.calculate_relative_coords(diff)

    def small_xiu_lian(self): # 世界地图界面-小修炼图标
        diff = (80, 1582, 253, 238)
        return self.calculate_relative_coords(diff)
    
    def ri_cheng(self): # 世界地图界面-日程图标
        diff = (28, 106, 124, 138)
        return self.calculate_relative_coords(diff)
    
    def ri_chang(self): # 世界地图界面-日常图标
        diff = (34, 398, 109, 136)
        return self.calculate_relative_coords(diff)
        
    def assistant(self): # 日常界面-小助手图标
        diff = (355, 1545, 128, 152)
        return self.calculate_relative_coords(diff)
    
    def huo_dong_bao_ming(self): # 小助手界面-活动报名图标
        diff = (159, 1577, 132, 121)
        return self.calculate_relative_coords(diff)
    
    def ri_chang_list(self): # 活动报名界面-日常列表
        diff = (94, 461, 955, 1020)
        return self.calculate_relative_coords(diff)
    
    def scroll_start_point(self): # 日常界面-鼠标滚动起始点
        diff = (382, 756, 0, 0)
        return self.calculate_relative_coords(diff)
    
    def price_in_store(self): # 在日常列表界面点击游历, 弹出购买界面时, 价格后面的数字的位置
        diff = (574, 1318, 72, 45)
        return self.calculate_relative_coords(diff)
    
    def current_lingshi(self):
        diff = (573, 1372, 166, 50)
        return self.calculate_relative_coords(diff)

    def buy_button_in_store(self): # 在日常列表界面点击游历, 弹出购买界面时, `购买并使用`按钮的位置
        diff = (376, 1426, 334, 123)
        return self.calculate_relative_coords(diff)
    
    def chat(self): # 世界地图界面-聊天图标
        diff = (33, 1458, 96, 62)
        return self.calculate_relative_coords(diff)
    
    def confirm_button_in_network_not_statble(self):
        diff = (392, 1227, 301, 96)
        return self.calculate_relative_coords(diff)

    def yang_chong_tou_hidden(self):
        diff = (537, 1702, 0, 0)
        return self.calculate_relative_coords(diff)
    
    def close_specifical_event(self): # 砸蛋
        diff = (1026, 28, 51, 72)
        return self.calculate_relative_coords(diff)
    
    def close_vip_fu_li(self): # vip福利
        diff = (453, 1297, 238, 65)
        return self.calculate_relative_coords(diff)
    
    def confirm_button_in_restart_game(self): # 重启游戏
        diff = (402, 1220, 302, 107)
        return self.calculate_relative_coords(diff)
    
class AssistantCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords: tuple, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)
    
    def run_button(self, sub_main_coords: tuple):
        diff = (738, 39, 123, 129)
        return self.calculate_relative_coords(diff, sub_main_coords)
    
    def duihuan_run_button(self):
        diff = (218, 1226, 306, 98)
        return self.calculate_relative_coords(diff)

class BaoMingCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords: tuple, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)
    
    def baoming_region(self):
        diff = (827, 239, 150, 1438)
        return self.calculate_relative_coords(diff)
    
    def baoming_lingshi(self):
        diff = (398, 1233, 303, 101)
        return self.calculate_relative_coords(diff)
    
class YouliCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)
    
    def youli_start(self): # 游历界面-前往游历按钮:
        diff = (392, 1526, 302, 98)
        return self.calculate_relative_coords(diff)
    
    def youli_end_one_time(self): # 游历界面-游历结束一次
        diff = (414, 1618, 265, 94)
        return self.calculate_relative_coords(diff)
    
    # def youli_exit(self): # 游历界面-点击该位置退出游历
    #     diff = (332, 1844, 0, 0)
    #     return self.calculate_relative_coords(diff)
    
    def youli_times_store(self): # 游历次数不足时, 弹出的购买界面
        diff = (107, 318, 858, 1226)
        return self.calculate_relative_coords(diff)

    def buy_button_in_store(self): # 在日常列表界面点击游历, 弹出购买界面时, `购买并使用`按钮的位置
        diff = (376, 1426, 334, 123)
        return self.calculate_relative_coords(diff)
    
    def price_in_store(self): # 在日常列表界面点击游历, 弹出购买界面时, 价格后面的数字的位置
        diff = (574, 1318, 72, 45)
        return self.calculate_relative_coords(diff)
    
    def current_lingshi(self):
        diff = (573, 1372, 166, 50)
        return self.calculate_relative_coords(diff)
    
class ShuangXiuCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)

    # def gongfashu_level(self, gongfashu_coords): # 日常界面-双修图标
    #     diff = (360, 131, 22, 27)
    #     return self.calculate_relative_coords(diff, gongfashu_coords)
    
    def yaoqing_daoyou(self): # 双修界面-邀请道友按钮
        diff = (478, 1447, 127, 127)
        return self.calculate_relative_coords(diff)
    
    def yaoqing_region(self): # 仙缘邀请界面-邀请区域
        diff = (772, 477, 193, 971)
        return self.calculate_relative_coords(diff)
    
    def go_to_xiulian(self): # 双修界面-前往修炼按钮
        diff = (287, 1644, 510, 101)
        return self.calculate_relative_coords(diff)

    def xianyuan_page(self): # 双修界面-仙缘界面
        diff = (314, 398, 162, 76)
        return self.calculate_relative_coords(diff)
    
    def remain_times(self):
        diff = (702, 1585, 41, 45)
        return self.calculate_relative_coords(diff)
    
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
    
class HongBaoCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords: tuple, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)

class HunDunLingTaCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)

class TiaoZhanXianYuanCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)

    def all_xian_yuan(self):
        diff=(324, 280, 160, 80)
        return self.calculate_relative_coords(diff)
    
    def qian_wang(self):
        diff=(430, 1527, 255, 96)
        return self.calculate_relative_coords(diff)
    
class LingShouCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)

    def region_for_check_mutli_challenge(self):
        diff = (449, 1705, 77, 69)
        return self.calculate_relative_coords(diff)

class BaiYeCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)

    def drag_from(self):
        diff = (804, 1312, 0, 0)
        return self.calculate_relative_coords(diff)
    
    def drag_to(self):
        diff = (504, 1312, 0, 0)
        return self.calculate_relative_coords(diff)
    
class ZhuiMoGuCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)

    def extract_challenge_times(self):
        diff = (449, 1705, 77, 69)
        return self.calculate_relative_coords(diff)
    
    def boss_icon(self):
        diff = (36, 774, 107, 136)
        return self.calculate_relative_coords(diff)
    
    def left_arrow(self):
        diff = (33, 526, 66, 138)
        return self.calculate_relative_coords(diff)
    
    def right_arrow(self):
        diff = (991, 526, 66, 138)
        return self.calculate_relative_coords(diff)
    
    def shou_ling_scroll_start_point(self):
        diff = (540, 960, 0, 0)
        return self.calculate_relative_coords(diff)
    
class GameControlCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)
    
    def menu_expansion(self):
        diff = (976, 1743, 52, 54)
        return self.calculate_relative_coords(diff)

    def confirm_in_exit_login_alert(self):
        diff = (582, 1223, 305, 103)
        return self.calculate_relative_coords(diff)
    
    def account_region(self):
        diff = (92, 802, 901, 148)
        return self.calculate_relative_coords(diff)
    
    def scroll_account_ls(self):
        diff = (534, 1044, 0, 0)
        return self.calculate_relative_coords(diff)

class QiXiMoJieCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)

    def confirm_button_in_last_qi_xi_alert(self):
        diff = (391, 1252, 303, 97)
        return self.calculate_relative_coords(diff)
    
    def confirm_button_in_chuang_jian_dui_wu(self):
        diff = (607, 1188, 303, 94)
        return self.calculate_relative_coords(diff)