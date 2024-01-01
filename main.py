import pyautogui
import numpy as np
import pandas as pd
from typing import Tuple
from datetime import datetime
from utils import get_game_page_coords, hide_yang_chong_tou, wait_for_evelen
from coords_manager import *
from event_executor import *
# from swy_coords_manager import *
# from swy_event_executor import *
from name_dict import task_name_dict, task_info_name_dict

from assistant import AssistantCoordsManager, AssistantExecutor
from xiu_lian import XiuLianCoordsManager, XiuLianExecutor
from you_li import YouliCoordsManager, YouLiExecutor
from fu_ben import FuBenCoordsManager, FuBenExecutor
from ling_shou import LingShouCoordsManager, LingShouExecutor
from lun_dao import LunDaoCoordsManager, LunDaoExecutor
from zhui_mo_gu import ZhuiMoGuCoordsManager, ZhuiMoGuExecutor
from shou_yuan_tan_mi import ShouYuanTanMiCoordsManager, ShouYuanTanMiExecutor
from mo_dao_ru_qing import MoDaoRuQingCoordsManager, MoDaoRuQingExecutor
from xian_meng_zheng_ba import XianMengZhengBaCoordsManager, XianMengZhengBaExecutor
from check_ri_chang import CheckRiChangCoordsManager, CheckRiChangExecutor
from shuang_xiu import ShuangXiuCoordsManager, ShuangXiuExecutor
from hun_dun_ling_ta import HunDunLingTaCoordsManager, HunDunLingTaExecutor
from tiao_zhan_xian_yuan import TiaoZhanXianYuanCoordsManager, TiaoZhanXianYuanExecutor
from pa_tian_ti import PaTianTiCoordsManager, PaTianTiExecutor
from bai_zu_gong_feng import BaiZuGongFengCoordsManager, BaiZuGongFengExecutor
from hong_bao import HongBaoCoordsManager, HongBaoExecutor
from ri_chang_chou_jiang import RiChangChouJiangCoordsManager, RiChangChouJiangExecutor
from game_control import GameControlCoordsManager, GameControlExecutor

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True
resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)

def daily_task(
    main_region_coords: Tuple[int, int, int, int],
    account_name: str,
    account_task_info: dict,
    ri_chang_chou_jiang: bool = True,
    xiu_lian: bool = True,
    qi_xi_mo_jie: bool = True,
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
    lun_dao: bool = True,
    shou_yuan_tan_mi: bool = False,
    mo_dao_ru_qing: bool = False,
    xian_meng_zheng_ba: bool = False,
    check_ri_chang: bool = True,
    pa_tian_ti: bool = False,
    bai_zu_gong_feng: bool = False,
    
):
    wei_mian = account_task_info['wei_mian']
    xiu_lian_buy_times = account_task_info['xiu_lian_buy_times']
    ling_ta_name = account_task_info['ling_ta_name']
    bai_ye_event_name = account_task_info['bai_ye_event_name']
    bai_ye_fa_ze_level = account_task_info['bai_ye_fa_ze_level']
    bai_zu_gong_feng_buy_times = account_task_info['bai_zu_gong_feng_buy_times']
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
    dao_chang_level = account_task_info['dao_chang_level']
    shou_yuan_tan_mi_server_nums = account_task_info.get('shou_yuan_tan_mi_server_nums', 1)
    mo_dao_ru_qing_server_nums = account_task_info.get('mo_dao_ru_qing_server_nums', 1)
    chou_jiang_event = account_task_info.get('chou_jiang_event', '灵缈探宝')

    shou_yuan_tan_mi_coords_manager = ShouYuanTanMiCoordsManager(main_region_coords) # 兽渊探秘
    mo_dao_ru_qing_coords_manager = MoDaoRuQingCoordsManager(main_region_coords) # 魔道入侵
    xian_meng_zheng_ba_coords_manager = XianMengZhengBaCoordsManager(main_region_coords) # 仙盟争霸

    ri_chang_chou_jiang_coords_manager = RiChangChouJiangCoordsManager(main_region_coords) # 日常抽奖
    xiu_lian_coords_manager = XiuLianCoordsManager(main_region_coords) # 修炼
    qi_xi_mo_jie_coords_manager = QiXiMoJieCoordsManager(main_region_coords) # 奇袭魔界
    hun_dun_ling_ta_coords_manager = HunDunLingTaCoordsManager(main_region_coords) # 混沌灵塔
    assistant_corrds_manager = AssistantCoordsManager(main_region_coords, resolution=resolution) # 小助手
    bao_ming_corrds_manager = BaoMingCoordsManager(main_region_coords, resolution=resolution) # 报名
    hong_bao_coords_manager = HongBaoCoordsManager(main_region_coords, resolution=resolution)# 红包
    bai_ye_coords_manager = BaiYeCoordsManager(main_region_coords) # 拜谒
    bai_zu_gong_feng_coords_manager = BaiZuGongFengCoordsManager(main_region_coords) # 百族供奉

    check_ri_chang_coords_manager = CheckRiChangCoordsManager(main_region_coords) # 检查日常

    youli_corrds_manager = YouliCoordsManager(main_region_coords, resolution=resolution) # 游历
    shuangxiu_corrds_manager = ShuangXiuCoordsManager(main_region_coords, resolution=resolution) # 双修
    fu_ben_coords_manager = FuBenCoordsManager(main_region_coords) # 副本
    tiao_zhan_xian_yuan_coords_manager = TiaoZhanXianYuanCoordsManager(main_region_coords) # 挑战仙缘
    ling_shou_coords_manager = LingShouCoordsManager(main_region_coords) # 灵兽
    zhui_mo_gu_coords_manager = ZhuiMoGuCoordsManager(main_region_coords) # 坠魔谷
    lun_dao_coords_manager = LunDaoCoordsManager(main_region_coords) # 论道

    shou_yuan_tan_mi_executor = ShouYuanTanMiExecutor(shou_yuan_tan_mi_coords_manager, server_nums=shou_yuan_tan_mi_server_nums, only_use_free_times=True) # 兽渊探秘
    mo_dao_ru_qing_executor = MoDaoRuQingExecutor(mo_dao_ru_qing_coords_manager, server_nums=mo_dao_ru_qing_server_nums) # 魔道入侵
    xian_meng_zheng_ba_executor = XianMengZhengBaExecutor(xian_meng_zheng_ba_coords_manager) # 仙盟争霸

    ri_chang_chou_jiang_executor = RiChangChouJiangExecutor(ri_chang_chou_jiang_coords_manager, chou_jiang_event=chou_jiang_event) # 日常抽奖
    xiu_lian_executor = XiuLianExecutor(xiu_lian_coords_manager, buy_times=xiu_lian_buy_times) # 修炼
    qi_xi_mo_jie_executor = QiXiMoJieExecutor(qi_xi_mo_jie_coords_manager) # 奇袭魔界
    hun_dun_ling_ta_executor = HunDunLingTaExecutor(hun_dun_ling_ta_coords_manager, ling_ta_name=ling_ta_name) # 弥罗之塔
    assistant_executor = AssistantExecutor(assistant_corrds_manager) # 小助手
    bao_ming_executor = BaoMingExecutor(bao_ming_corrds_manager) # 报名
    hong_bao_executor = HongBaoExecutor(hong_bao_coords_manager) # 红包
    bai_ye_executor = BaiYeExecutor(bai_ye_coords_manager, event_name=bai_ye_event_name, fa_ze_level=bai_ye_fa_ze_level) # 拜谒
    bai_zu_gong_feng_executor = BaiZuGongFengExecutor(bai_zu_gong_feng_coords_manager, buy_times=bai_zu_gong_feng_buy_times) # 百族供奉

    check_ri_chang_executor = CheckRiChangExecutor(check_ri_chang_coords_manager, account_name) # 检查日常

    shuangxiu_executor = ShuangXiuExecutor(shuangxiu_corrds_manager, gongfashu_name=shuangxiu_gongfashu_name) # 双修
    tiao_zhan_xian_yuan_executor = TiaoZhanXianYuanExecutor(tiao_zhan_xian_yuan_coords_manager, xian_yuan_role_name=tiao_zhan_xian_yuan_role_name, wei_mian=wei_mian) # 挑战仙缘
    youli_executor = YouLiExecutor(youli_corrds_manager, place_name=youli_place_name, buy_times=youli_buy_times) # 游历
    ling_shou_executor = LingShouExecutor(ling_shou_coords_manager, buy_times=ling_shou_buy_times, to_save_times=ling_shou_to_save_times) # 灵兽
    zhui_mo_gu_executor = ZhuiMoGuExecutor(zhui_mo_gu_coords_manager, profession_name=profession_name, max_level=zhui_mo_gu_max_level, wei_mian=wei_mian) # 坠魔谷
    fuben_executor = FuBenExecutor(fu_ben_coords_manager, fuben_name=fuben_name, buy_times=fuben_buy_times) # 副本
    lun_dao_executor = LunDaoExecutor(lun_dao_coords_manager, dao_chang_level=dao_chang_level) # 论道

    pa_tian_ti_coords_manager = PaTianTiCoordsManager(main_region_coords) # 爬天梯
    pa_tian_ti_executor = PaTianTiExecutor(pa_tian_ti_coords_manager) # 爬天梯

    all_executor = {

        '论道': (lun_dao_executor, lun_dao),
        '奇袭魔界': (qi_xi_mo_jie_executor, qi_xi_mo_jie),
        '日常抽奖': (ri_chang_chou_jiang_executor, ri_chang_chou_jiang), # 日常抽奖

        '报名': (bao_ming_executor, bao_ming),
        '红包': (hong_bao_executor, hong_bao),
        '小助手': (assistant_executor, assistant),
        '修炼': (xiu_lian_executor, xiu_lian),
        '拜谒': (bai_ye_executor, bai_ye),
        '百族供奉': (bai_zu_gong_feng_executor, bai_zu_gong_feng),

        '混沌灵塔_爬塔': (hun_dun_ling_ta_executor, hun_dun_ling_ta),
        '混沌灵塔_扫荡': (hun_dun_ling_ta_executor, hun_dun_ling_ta),

        '挑战仙缘': (tiao_zhan_xian_yuan_executor, tiao_zhan_xian_yuan),
        '游历': (youli_executor, youli),
        '双修': (shuangxiu_executor, shuangxiu),
        '灵兽': (ling_shou_executor, ling_shou),
        '副本': (fuben_executor, fuben),
        '坠魔谷': (zhui_mo_gu_executor, zhui_mo_gu),
        
        '兽渊探秘': (shou_yuan_tan_mi_executor, shou_yuan_tan_mi),
        '魔道入侵': (mo_dao_ru_qing_executor, mo_dao_ru_qing),
        '仙盟争霸': (xian_meng_zheng_ba_executor, xian_meng_zheng_ba),

        '爬天梯': (pa_tian_ti_executor, pa_tian_ti),

        '检查日常': (check_ri_chang_executor, check_ri_chang),
    }

    hide_yang_chong_tou(
        main_region_coords=main_region_coords,
        hidden_region_coords=hun_dun_ling_ta_coords_manager.yang_chong_tou_hidden()[:2]
    )

    for executor_name, if_execute in all_executor.items():
        executor, if_execute = if_execute
        if if_execute:
            wait_for_evelen()

            start_time = datetime.now()
            try:
                if executor_name in ['论道', '兽渊探秘', '魔道入侵']:
                    if datetime.now().hour < 11: #  11点之前不执行
                        print(f'{executor_name}未到执行时间')
                        break
                
                if executor_name == '混沌灵塔_爬塔':
                    executor.go_up()
                elif executor_name == '混沌灵塔_扫荡':
                    executor.sao_dang()
                else:
                    executor.execute()
                
                print(f'{executor_name}执行完毕')

            except Exception as e:
                print(f'{executor_name}执行失败: {e}')
                with open('error.txt', 'a', encoding='utf-8') as f:
                    current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
                    # f.write(
                    #     f'\n------------------------------------------------\n{current_time}-{account_name}-{executor_name}:{e}\n------------------------------------------------\n'
                    # )
                    f.write(
                        f'\n{current_time}-{account_name}-{executor_name}:{e}\n'
                    )

            end_time = datetime.now()
            print(f'{executor_name}执行时间: {end_time - start_time}')
            with open('time.txt', 'a', encoding='utf-8') as f:
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
                cost_time = (end_time - start_time).seconds
                # f.write(
                #     f'\n------------------------------------------------\n{current_time}-{account_name}-{executor_name}-执行时间: {cost_time}秒\n------------------------------------------------\n'
                # )
                f.write(
                    f'\n{current_time}-{account_name}-{executor_name}-执行时间: {cost_time}秒\n'
                )

            executor.go_to_world()

if __name__ == '__main__':
    
    try:
        main_region_coords = get_game_page_coords(resolution = resolution)
    except Exception as e:
        print(f"未定位到游戏界面!")

    game_coords_manager = GameControlCoordsManager(main_region_coords)
    root_dir = 'C:/Users/zyf13/My Drive/auto_xiu_xian'
    file_name = 'game_execute_info.xlsx'
    file_path = os.path.join(root_dir, file_name)

    # accounts
    accounts = pd.read_excel(file_path, sheet_name='accounts')

    accounts = accounts[accounts['execute'] == 1]
    account_name_ls = accounts['account_names'].tolist()
    
    # users_info
    account_task_info_df = pd.read_excel(file_path, sheet_name='users_info')
    account_task_info_df.set_index('users_name', inplace=True)
    account_task_info_df.rename(columns=task_info_name_dict, inplace=True)
    
    # task_execute
    task_execute_df = pd.read_excel(file_path, sheet_name='task_execute')
    task_execute_df.set_index('users_name', inplace=True)
    task_execute_df.rename(columns=task_name_dict, inplace=True)

    for account_name in account_name_ls:

        print(f'开始执行{account_name}的日常任务')
        account_task_info = account_task_info_df.loc[account_name].to_dict()
        account = account_task_info['users']

        execute_info = task_execute_df.loc[account_name].to_dict()
        
        try:
            game_executor = GameControlExecutor(game_coords_manager, account_name=account_name, account=account)
            game_executor.execute()
        except Exception as e:
            print(f'{account_name}执行失败: {e}')

        daily_task(main_region_coords, account_name=account_name, account_task_info=account_task_info, **execute_info)
