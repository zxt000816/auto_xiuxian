import pyautogui
import numpy as np
from typing import Tuple
from utils import get_game_page_coords, get_region_coords, get_region_coords_by_multi_imgs
from coords_manager import *
from event_executor import *

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True
resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)

try:
    main_region_coords = get_game_page_coords(resolution = resolution)
except Exception as e:
    print(f"未定位到游戏界面!")

def daily_task(
    account_name: str,
    account_task_info: dict,
    hun_dun_ling_ta: bool = True,
    assistant: bool = True,
    bao_ming: bool = True,
    hong_bao: bool = True,
    bai_ye: bool = True,
    youli: bool = True,
    shuangxiu: bool = True,
    tiao_zhan_xian_yuan: bool = True,
    ling_shou: bool = True,
    fuben: bool = True,
    zhui_mo_gu: bool = True,
):
    ling_ta_name = account_task_info['ling_ta_name']
    bai_ye_event_name = account_task_info['bai_ye_event_name']
    bai_ye_fa_ze_level = account_task_info['bai_ye_fa_ze_level']
    shuangxiu_gongfashu_name = account_task_info['shuangxiu_gongfashu_name']
    tiao_zhan_xian_yuan_role_name = account_task_info['tiao_zhan_xian_yuan_role_name']
    youli_place_name = account_task_info['youli_place_name']
    youli_buy_times = account_task_info['youli_buy_times']
    ling_shou_buy_times = account_task_info['ling_shou_buy_times']
    ling_shou_to_save_times = account_task_info['ling_shou_to_save_times']
    fuben_name = account_task_info['fuben_name']
    fuben_buy_times = account_task_info['fuben_buy_times']
    profession_name = account_task_info['profession_name']
    zhui_mo_gu_max_level = account_task_info['zhui_mo_gu_max_level']

    try:
        hun_dun_ling_ta_coords_manager = HunDunLingTaCoordsManager(main_region_coords)
        assistant_corrds_manager = AssistantCoordsManager(main_region_coords, resolution=resolution)
        bao_ming_corrds_manager = BaoMingCoordsManager(main_region_coords, resolution=resolution)
        hong_bao_coords_manager = HongBaoCoordsManager(main_region_coords, resolution=resolution)
        bai_ye_coords_manager = BaiYeCoordsManager(main_region_coords)

        youli_corrds_manager = YouliCoordsManager(main_region_coords, resolution=resolution)
        shuangxiu_corrds_manager = ShuangXiuCoordsManager(main_region_coords, resolution=resolution)
        fu_ben_coords_manager = FuBenCoordsManager(main_region_coords)
        tiao_zhan_xian_yuan_coords_manager = TiaoZhanXianYuanCoordsManager(main_region_coords)
        ling_shou_coords_manager = LingShouCoordsManager(main_region_coords)
        zhui_mo_gu_coords_manager = ZhuiMoGuCoordsManager(main_region_coords)

        hun_dun_ling_ta_executor = HunDunLingTaExecutor(hun_dun_ling_ta_coords_manager, ling_ta_name=ling_ta_name) # 弥罗之塔
        assistant_executor = AssistantExecutor(assistant_corrds_manager)
        bao_ming_executor = BaoMingExecutor(bao_ming_corrds_manager)
        hong_bao_executor = HongBaoExecutor(hong_bao_coords_manager)
        bai_ye_executor = BaiYeExecutor(bai_ye_coords_manager, event_name=bai_ye_event_name, fa_ze_level=bai_ye_fa_ze_level)

        shuangxiu_executor = ShuangXiuExecutor(shuangxiu_corrds_manager, gongfashu_name=shuangxiu_gongfashu_name)
        tiao_zhan_xian_yuan_executor = TiaoZhanXianYuanExecutor(tiao_zhan_xian_yuan_coords_manager, xian_yuan_role_name=tiao_zhan_xian_yuan_role_name)
        youli_executor = YouLiExecutor(youli_corrds_manager, place_name=youli_place_name, buy_times=youli_buy_times)
        ling_shou_executor = LingShouExecutor(ling_shou_coords_manager, buy_times=ling_shou_buy_times, to_save_times=ling_shou_to_save_times)
        fuben_executor = FuBenExecutor(fu_ben_coords_manager, fuben_name=fuben_name, buy_times=fuben_buy_times)
        zhui_mo_gu_executor = ZhuiMoGuExecutor(zhui_mo_gu_coords_manager, profession_name=profession_name, max_level=zhui_mo_gu_max_level)

        all_executor = {
            'hun_dun_ling_ta_executor': (hun_dun_ling_ta_executor, hun_dun_ling_ta),
            'assistant_executor': (assistant_executor, assistant),
            'bao_ming_executor': (bao_ming_executor, bao_ming),
            'hong_bao_executor': (hong_bao_executor, hong_bao),
            'bai_ye_executor': (bai_ye_executor, bai_ye),
            'youli_executor': (youli_executor, youli),
            'shuangxiu_executor': (shuangxiu_executor, shuangxiu),
            'tiao_zhan_xian_yuan_executor': (tiao_zhan_xian_yuan_executor, tiao_zhan_xian_yuan),
            'ling_shou_executor': (ling_shou_executor, ling_shou),
            'fuben_executor': (fuben_executor, fuben),
            'zhui_mo_gu_executor': (zhui_mo_gu_executor, zhui_mo_gu),
        }

        for executor_name, if_execute in all_executor.items():
            executor, if_execute = if_execute
            if if_execute:
                executor.execute()
                print(f'{executor_name}执行完毕')

    except Exception as e:
        print(e)
        print('程序异常，退出')

if __name__ == '__main__':
    game_coords_manager = GameControlCoordsManager(main_region_coords)
    account_name_ls = ['小七', '初心', '野菜花', '白起(仙山)', '白起(黄河)', '晴雪']

    account_task_info = {
        '野菜花': {
            'ling_ta_name': '弥罗之塔',
            'bai_ye_event_name': '兽渊',
            'bai_ye_fa_ze_level': 1,
            'shuangxiu_gongfashu_name': '六欲练心',
            'tiao_zhan_xian_yuan_role_name': '势不两立',
            'youli_place_name': '南疆',
            'youli_buy_times': 0,
            'ling_shou_buy_times': 2,
            'ling_shou_to_save_times': True,
            'fuben_name': '昆吾山',
            'fuben_buy_times': 0,
            'profession_name': '法',
            'zhui_mo_gu_max_level': '元婴-后期-十层'
        },
        '白起(仙山)': {
            'ling_ta_name': '弥罗之塔',
            'bai_ye_event_name': '兽渊',
            'bai_ye_fa_ze_level': 1,
            'shuangxiu_gongfashu_name': '六欲练心',
            'tiao_zhan_xian_yuan_role_name': '势不两立',
            'youli_place_name': '南疆',
            'youli_buy_times': 2,
            'ling_shou_buy_times': 2,
            'ling_shou_to_save_times': True,
            'fuben_name': '昆吾山',
            'fuben_buy_times': 2,
            'profession_name': '魔',
            'zhui_mo_gu_max_level': '化神-中期-十层'
        },
        '白起(黄河)': {
            'ling_ta_name': '弥罗之塔',
            'bai_ye_event_name': '兽渊',
            'bai_ye_fa_ze_level': 1,
            'shuangxiu_gongfashu_name': '六欲练心',
            'tiao_zhan_xian_yuan_role_name': '势不两立',
            'youli_place_name': '南疆',
            'youli_buy_times': 2,
            'ling_shou_buy_times': 2,
            'ling_shou_to_save_times': True,
            'fuben_name': '昆吾山',
            'fuben_buy_times': 2,
            'profession_name': '体',
            'zhui_mo_gu_max_level': '化神-中期-十层'
        },
        '晴雪': {
            'ling_ta_name': '弥罗之塔',
            'bai_ye_event_name': '兽渊',
            'bai_ye_fa_ze_level': 1,
            'shuangxiu_gongfashu_name': '六欲练心',
            'tiao_zhan_xian_yuan_role_name': '势不两立',
            'youli_place_name': '南疆',
            'youli_buy_times': 0,
            'ling_shou_buy_times': 2,
            'ling_shou_to_save_times': True,
            'fuben_name': '昆吾山',
            'fuben_buy_times': 0,
            'profession_name': '剑',
            'zhui_mo_gu_max_level': '元婴-后期-十层'
        },
        '初心': {
            'ling_ta_name': '弥罗之塔',
            'bai_ye_event_name': '兽渊',
            'bai_ye_fa_ze_level': 1,
            'shuangxiu_gongfashu_name': '六欲练心',
            'tiao_zhan_xian_yuan_role_name': '势不两立',
            'youli_place_name': '南疆',
            'youli_buy_times': 2,
            'ling_shou_buy_times': 2,
            'ling_shou_to_save_times': True,
            'fuben_name': '昆吾山',
            'fuben_buy_times': 2,
            'profession_name': '剑',
            'zhui_mo_gu_max_level': '化神-前期-十层'
        },
        '小七': {
            'ling_ta_name': '弥罗之塔',
            'bai_ye_event_name': '兽渊',
            'bai_ye_fa_ze_level': 1,
            'shuangxiu_gongfashu_name': '六欲练心',
            'tiao_zhan_xian_yuan_role_name': '势不两立',
            'youli_place_name': '南疆',
            'youli_buy_times': 2,
            'ling_shou_buy_times': 2,
            'ling_shou_to_save_times': True,
            'fuben_name': '昆吾山',
            'fuben_buy_times': 2,
            'profession_name': '剑',
            'zhui_mo_gu_max_level': '化神-前期-十层'
        },

    }

    for account_name in account_name_ls:
        print(f'开始执行{account_name}的日常任务')
        print(f'账号信息：{account_task_info[account_name]}')
        game_executor = GameControlExecutor(game_coords_manager, account_name=account_name)
        game_executor.execute()
        
        daily_task(
            account_name = account_name, 
            account_task_info = account_task_info[account_name], 
            hun_dun_ling_ta = False,
            assistant = False,
            bao_ming = False,
            hong_bao = False,
            bai_ye = False,
            youli = True,
            shuangxiu = False,
            tiao_zhan_xian_yuan = False,
            ling_shou = False,
            fuben = False,
            zhui_mo_gu = False,
        )

