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
    
    def create_image_path(self, index, root_dir='C:/Users/zyf13/My Drive/auto_xiu_xian'):
        _root_dir = os.path.join(root_dir, self.account_name)
        if not os.path.exists(_root_dir):
            os.mkdir(_root_dir)

        date = datetime.now().strftime('%Y-%m-%d')
        img_name = f'{self.account_name}_{date}_{index}.png'
        return os.path.join(_root_dir, img_name)

    def save_img(self, img_coords, img_path):
        img = pyautogui.screenshot(region=img_coords)
        print(f'save img to {img_path}')
        img.save(img_path)

    def scroll_serval_times(self, times):
        for i in range(times):
            pyautogui.scroll(-200)
            time.sleep(0.1)
    
    def execute(self):

        self.go_to_world()

        self.click_ri_chang()

        for index in range(1, 4+1):
            self.save_img(img_coords=self.main_region_coords, img_path=self.create_image_path(index))
            pyautogui.moveTo(self.cm.scroll_start_point()[:2])
            pyautogui.scroll(-300)
            time.sleep(3)

if __name__ == '__main__':
    main_region_coords = get_game_page_coords(resolution = resolution)

    coords_manager = CheckRiChangCoordsManager(main_region_coords)
    executor = CheckRiChangExecutor(coords_manager, account_name='test')

    executor.execute()
