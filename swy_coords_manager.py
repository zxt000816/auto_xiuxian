from coords_manager import BaseCoordsManager

class ShouYuanTanMiCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)

    def shou_yuan_menus(self):
        diff = (351, 1567, 662, 282)
        return self.calculate_relative_coords(diff)
    
    def task_menus(self):
        diff = (83, 219, 564, 102)
        return self.calculate_relative_coords(diff)
    
    def ling_qu_pos(self):
        diff = (546, 439, 0, 0)
        return self.calculate_relative_coords(diff)
    
    def confirm_button_in_alert_for_next_region(self):
        diff = (580, 1223, 308, 100)
        return self.calculate_relative_coords(diff)
    
    def if_only_use_free_times(self):
        diff = (258, 1213, 94, 91)
        return self.calculate_relative_coords(diff)
    
    def do_not_stop(self):
        diff = (262, 1303, 83, 83)
        return self.calculate_relative_coords(diff)
    
    def confirm_button_in_auto_tan_cha_over(self):
        diff = (402, 1227, 302, 96)
        return self.calculate_relative_coords(diff)