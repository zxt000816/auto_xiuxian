import pyautogui
import numpy as np
from typing import Tuple
from utils import get_game_page_coords, get_region_coords, get_region_coords_by_multi_imgs
from coords_manager import AssistantCoordsManager, BaoMingCoordsManager, YouliCoordsManager,\
                           ShuangXiuCoordsManager, FuBenCoordsManager, HongBaoCoordsManager,\
                           HunDunLingTaCoordsManager, TiaoZhanXianYuanCoordsManager, LingShouCoordsManager
from event_executor import AssistantExecutor, BaoMingExecutor, YouLiExecutor, ShuangXiuExecutor,\
                           FuBenExecutor, HongBaoExecutor, HunDunLingTaExecutor, TiaoZhanXianYuanExecutor, \
                           LingShouExecutor

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True
resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)

try:
    main_region_coords = get_game_page_coords(resolution = resolution)
except Exception as e:
    print(f"未定位到游戏界面!")

try:
    hun_dun_ling_ta_coords_manager = HunDunLingTaCoordsManager(main_region_coords)
    assistant_corrds_manager = AssistantCoordsManager(main_region_coords, resolution=resolution)
    bao_ming_corrds_manager = BaoMingCoordsManager(main_region_coords, resolution=resolution)
    hong_bao_coords_manager = HongBaoCoordsManager(main_region_coords, resolution=resolution)
    youli_corrds_manager = YouliCoordsManager(main_region_coords, resolution=resolution)
    shuangxiu_corrds_manager = ShuangXiuCoordsManager(main_region_coords, resolution=resolution)
    fu_ben_coords_manager = FuBenCoordsManager(main_region_coords)
    tiao_zhan_xian_yuan_coords_manager = TiaoZhanXianYuanCoordsManager(main_region_coords)
    ling_shou_coords_manager = LingShouCoordsManager(main_region_coords)
    
    hun_dun_ling_ta_executor = HunDunLingTaExecutor(hun_dun_ling_ta_coords_manager, ling_ta_name='弥罗之塔')
    assistant_executor = AssistantExecutor(assistant_corrds_manager)
    bao_ming_executor = BaoMingExecutor(bao_ming_corrds_manager)
    hong_bao_executor = HongBaoExecutor(hong_bao_coords_manager)
    youli_executor = YouLiExecutor(youli_corrds_manager, place_name='南疆', buy_times=3)
    shuangxiu_executor = ShuangXiuExecutor(shuangxiu_corrds_manager, gongfashu_name='百花烟雨')
    fuben_executor = FuBenExecutor(fu_ben_coords_manager, fuben_name='昆吾山', buy_times=3)
    tiao_zhan_xian_yuan_executor = TiaoZhanXianYuanExecutor(tiao_zhan_xian_yuan_coords_manager, xian_yuan_role_name='尸魈')
    ling_shou_executor = LingShouExecutor(ling_shou_coords_manager, buy_times=3)

    hun_dun_ling_ta_executor.execute()
    assistant_executor.execute()
    bao_ming_executor.execute()
    hong_bao_executor.execute()
    youli_executor.execute()
    shuangxiu_executor.execute()
    fuben_executor.execute()
    tiao_zhan_xian_yuan_executor.execute()
    ling_shou_executor.execute()

except Exception as e:
    print(e)
    print('程序异常，退出')
