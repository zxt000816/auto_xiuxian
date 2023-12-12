import pyautogui
from utils import get_region_coords, get_game_page_coords


main_region_coords = get_game_page_coords(
    resolution = (1080, 1920)
)

yang_chong_tou_coords = get_region_coords(
    'yang_chong_tou',
    main_region_coords,
    confidence=0.7,
)


pyautogui.screenshot(region=yang_chong_tou_coords)


center_coords = (yang_chong_tou_coords[0] + yang_chong_tou_coords[2] / 2, yang_chong_tou_coords[1] + yang_chong_tou_coords[3] / 2)

pyautogui.moveTo(center_coords[0], center_coords[1])

pyautogui.dragTo(2770, 1331, duration=2)

(3244, 1825, 0, 0)

main_region_coords

(3244 - main_region_coords[0], 1825 - main_region_coords[1], 0, 0)