class BaseCoordsManager:
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        self.main_region_coords = main_region_coords
        self.x = main_region_coords[0]
        self.y = main_region_coords[1]
        self.width = main_region_coords[2]
        self.height = main_region_coords[3]
        self.resolution = resolution
    
    def calculate_relative_coords(self, diff, specific_region_coords=None):
        if specific_region_coords is None:
            left_top_x = self.x + diff[0]
            left_top_y = self.y + diff[1]
            width = diff[2]
            height = diff[3]
            return (left_top_x, left_top_y, width, height)
        else:
            left_top_x = specific_region_coords[0] + diff[0]
            left_top_y = specific_region_coords[1] + diff[1]
            width = diff[2]
            height = diff[3]
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
    
class AssistantCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords: tuple):
        super().__init__(main_region_coords)
    
    def run_button(self, sub_main_coords: tuple):
        diff = (738, 39, 123, 129)
        return self.calculate_relative_coords(diff, sub_main_coords)
    
    def duihuan_run_button(self):
        diff = (218, 1226, 306, 98)
        return self.calculate_relative_coords(diff)

class BaoMingCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords: tuple):
        super().__init__(main_region_coords)
    
    def baoming_region(self):
        diff = (827, 239, 150, 1438)
        return self.calculate_relative_coords(diff)
    
    def baoming_lingshi(self):
        diff = (398, 1233, 303, 101)
        return self.calculate_relative_coords(diff)

class ShuangXiuCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)

    def gongfashu_level(self, gongfashu_coords): # 日常界面-双修图标
        diff = (360, 131, 22, 27)
        return self.calculate_relative_coords(diff, gongfashu_coords)
    
    def back(self):
        diff = (60, 1792, 72, 71)
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