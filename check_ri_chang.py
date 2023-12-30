import pyautogui
from utils import *
from swy_coords_manager import BaseCoordsManager
from swy_event_executor import BaseExecutor
from xiuxian_exception import *
from datetime import datetime

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True
resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)

class CheckRiChangCoordsManager(BaseCoordsManager):
    def __init__(self, main_region_coords, resolution=(1080, 1920)):
        super().__init__(main_region_coords, resolution)

    def chu_wu_dai_coords(self):
        diff = (941, 1583, 119, 132)
        return self.calculate_relative_coords(diff)
    
    def bei_bao_scroll_start_point(self):
        diff = (561, 668, 0, 0)
        return self.calculate_relative_coords(diff)

class CheckRiChangExecutor(BaseExecutor):
    def __init__(self, cm: CheckRiChangCoordsManager, account_name):
        super().__init__(cm)
        self.cm = cm
        self.account_name = account_name

    @wait_region
    def get_xian_meng_zheng_ba_coords(self, wait_time, target_region, is_to_click, to_raise_exception):
        return get_region_coords(
            'xian_meng_zheng_ba',
            main_region_coords=self.main_region_coords,
            confidence=0.8,
            cat_dir=self.cat_dir ,
        )
    
    def create_image_path(self, target_name, index, root_dir='C:/Users/zyf13/My Drive/auto_xiu_xian'):
        date = datetime.now().strftime('%Y-%m-%d')

        _root_dir = os.path.join(root_dir, date, self.account_name)
        if not os.path.exists(_root_dir):
            os.makedirs(_root_dir)
        
        img_name = f'{self.account_name}_{target_name}_{index}.png'
        return os.path.join(_root_dir, img_name)

    def save_img(self, img_coords, img_path):
        img = pyautogui.screenshot(region=img_coords)
        print(f'save img to {img_path}')
        img.save(img_path)
    
    def execute(self):

        self.go_to_world()

        self.click_ri_chang()

        scroll_length = self.calculate_scroll_length(-300)
        for index in range(1, 4+1):
            self.save_img(img_coords=self.main_region_coords, img_path=self.create_image_path('日常', index))
            # pyautogui.moveTo(self.cm.scroll_start_point()[:2])
            pyautogui.moveTo(self.cm.bei_bao_scroll_start_point()[:2])
            # pyautogui.scroll(-300 * self.coords_manager.y_ratio)
            pyautogui.scroll(scroll_length)
            time.sleep(3)

        self.go_to_world()

        click_region(self.cm.chu_wu_dai_coords()) 
        for index in range(1, 14+1):
            self.save_img(img_coords=self.main_region_coords, img_path=self.create_image_path('背包', index))
            pyautogui.moveTo(self.cm.bei_bao_scroll_start_point()[:2])
            pyautogui.scroll(scroll_length)
            time.sleep(3)

if __name__ == '__main__':
    main_region_coords = get_game_page_coords(resolution = resolution)

    coords_manager = CheckRiChangCoordsManager(main_region_coords)
    executor = CheckRiChangExecutor(coords_manager, account_name='test')

    executor.execute()
