import os
import pyautogui
import pandas as pd
from typing import Tuple
from datetime import datetime
import time
from name_dict import task_name_dict, task_info_name_dict
# from dotenv import load_dotenv

pyautogui.PAUSE = 0.01
pyautogui.FAILSAFE = True

# load_dotenv()

def daily_task(
    main_region_coords: Tuple[int, int, int, int],
    account_name: str,
    account_task_info: dict,
    ri_chang_chou_jiang: bool = True,
    xiu_lian: bool = True,
    qi_xi_mo_jie: bool = True,
    hun_dun_ling_ta_sao_dang: bool = True, # 混沌灵塔扫荡
    hun_dun_ling_ta_go_up: bool = True, # 混沌灵塔爬塔
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
    xu_tian_dian: bool = False,
    yun_meng_shi_jian: bool = False,
    xian_meng_zheng_ba: bool = False,
    pa_tian_ti: bool = False,
    bai_zu_gong_feng: bool = False,
    check_ri_chang: bool = True,
    check_all_tasks: bool = False,
    resolution: Tuple[int, int] = (1080, 1920),
):
    wei_mian = account_task_info['wei_mian']
    if wei_mian == '人界':
        bai_zu_gong_feng = False

    xian_yuan_wei_mian = account_task_info['xian_yuan_wei_mian']
    shou_ling_wei_mian = account_task_info['shou_ling_wei_mian']

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
    yun_meng_shi_jian_server_nums = account_task_info.get('yun_meng_shi_jian_server_nums', 1)
    chou_jiang_event = account_task_info.get('chou_jiang_event', '灵缈探宝')

    shou_yuan_tan_mi_coords_manager = ShouYuanTanMiCoordsManager(main_region_coords, resolution=resolution) # 兽渊探秘
    mo_dao_ru_qing_coords_manager = MoDaoRuQingCoordsManager(main_region_coords, resolution=resolution) # 魔道入侵
    xu_tian_dian_coords_manager = XuTianDianCoordsManager(main_region_coords, resolution=resolution) # 虚天殿
    yun_meng_shi_jian_coords_manager = YunMengShiJianCoordsManager(main_region_coords, resolution=resolution) # 云梦试剑

    xian_meng_zheng_ba_coords_manager = XianMengZhengBaCoordsManager(main_region_coords, resolution=resolution) # 仙盟争霸

    ri_chang_chou_jiang_coords_manager = RiChangChouJiangCoordsManager(main_region_coords, resolution=resolution) # 日常抽奖
    xiu_lian_coords_manager = XiuLianCoordsManager(main_region_coords, resolution=resolution) # 修炼
    qi_xi_mo_jie_coords_manager = QiXiMoJieCoordsManager(main_region_coords, resolution=resolution) # 奇袭魔界
    hun_dun_ling_ta_coords_manager = HunDunLingTaCoordsManager(main_region_coords, resolution=resolution) # 混沌灵塔
    assistant_corrds_manager = AssistantCoordsManager(main_region_coords, resolution=resolution) # 小助手
    bao_ming_corrds_manager = BaoMingCoordsManager(main_region_coords, resolution=resolution) # 报名
    hong_bao_coords_manager = HongBaoCoordsManager(main_region_coords, resolution=resolution)# 红包
    bai_ye_coords_manager = BaiYeCoordsManager(main_region_coords, resolution=resolution) # 拜谒
    bai_zu_gong_feng_coords_manager = BaiZuGongFengCoordsManager(main_region_coords, resolution=resolution) # 百族供奉

    check_ri_chang_coords_manager = CheckRiChangCoordsManager(main_region_coords, resolution=resolution) # 检查日常
    check_all_tasks_coords_manager = CheckAllTasksCoordsManager(main_region_coords, resolution=resolution) # 检查任务

    youli_corrds_manager = YouliCoordsManager(main_region_coords, resolution=resolution) # 游历
    shuangxiu_corrds_manager = ShuangXiuCoordsManager(main_region_coords, resolution=resolution) # 双修
    fu_ben_coords_manager = FuBenCoordsManager(main_region_coords, resolution=resolution) # 副本
    tiao_zhan_xian_yuan_coords_manager = TiaoZhanXianYuanCoordsManager(main_region_coords, resolution=resolution) # 挑战仙缘
    ling_shou_coords_manager = LingShouCoordsManager(main_region_coords, resolution=resolution) # 灵兽
    zhui_mo_gu_coords_manager = ZhuiMoGuCoordsManager(main_region_coords, resolution=resolution) # 坠魔谷
    lun_dao_coords_manager = LunDaoCoordsManager(main_region_coords, resolution=resolution) # 论道

    shou_yuan_tan_mi_executor = ShouYuanTanMiExecutor(shou_yuan_tan_mi_coords_manager, server_nums=shou_yuan_tan_mi_server_nums, only_use_free_times=True) # 兽渊探秘
    mo_dao_ru_qing_executor = MoDaoRuQingExecutor(mo_dao_ru_qing_coords_manager, server_nums=mo_dao_ru_qing_server_nums) # 魔道入侵
    xu_tian_dian_executor = XuTianDianExecutor(xu_tian_dian_coords_manager) # 虚天殿
    yun_meng_shi_jian_executor = YunMengShiJianExecutor(yun_meng_shi_jian_coords_manager, server_nums=yun_meng_shi_jian_server_nums) # 云梦试剑

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
    check_all_tasks_executor = CheckAllTasksExecutor(check_all_tasks_coords_manager) # 检查任务

    shuangxiu_executor = ShuangXiuExecutor(shuangxiu_corrds_manager, gongfashu_name=shuangxiu_gongfashu_name) # 双修
    tiao_zhan_xian_yuan_executor = TiaoZhanXianYuanExecutor(tiao_zhan_xian_yuan_coords_manager, xian_yuan_role_name=tiao_zhan_xian_yuan_role_name, wei_mian=xian_yuan_wei_mian) # 挑战仙缘
    youli_executor = YouLiExecutor(youli_corrds_manager, place_name=youli_place_name, buy_times=youli_buy_times) # 游历
    ling_shou_executor = LingShouExecutor(ling_shou_coords_manager, buy_times=ling_shou_buy_times, to_save_times=ling_shou_to_save_times) # 灵兽
    zhui_mo_gu_executor = ZhuiMoGuExecutor(zhui_mo_gu_coords_manager, profession_name=profession_name, max_level=zhui_mo_gu_max_level, wei_mian=shou_ling_wei_mian) # 坠魔谷
    fuben_executor = FuBenExecutor(fu_ben_coords_manager, fuben_name=fuben_name, buy_times=fuben_buy_times) # 副本
    lun_dao_executor = LunDaoExecutor(lun_dao_coords_manager, dao_chang_level=dao_chang_level) # 论道

    pa_tian_ti_coords_manager = PaTianTiCoordsManager(main_region_coords) # 爬天梯
    pa_tian_ti_executor = PaTianTiExecutor(pa_tian_ti_coords_manager) # 爬天梯

    if check_all_tasks:
        try:
            finished_tasks = check_all_tasks_executor.execute()
            print(f'完成的任务: {finished_tasks}')
            # 用户设置为True, 任务检查为True时, 才会执行
            ling_shou = all([ling_shou, finished_tasks.get('ling_shou', True)]) 
            youli = all([youli, finished_tasks.get('youli', True)])
            fuben = all([fuben, finished_tasks.get('fuben', True)])
            bai_zu_gong_feng = all([bai_zu_gong_feng, finished_tasks.get('bai_zu_gong_feng', True)])
            shuangxiu = all([shuangxiu, finished_tasks.get('shuangxiu', True)])
            xiu_lian = all([xiu_lian, finished_tasks.get('xiu_lian', True)])
            tiao_zhan_xian_yuan = all([tiao_zhan_xian_yuan, finished_tasks.get('tiao_zhan_xian_yuan', True)])
            zhui_mo_gu = all([zhui_mo_gu, finished_tasks.get('zhui_mo_gu', True)])
            # lun_dao = all([lun_dao, finished_tasks.get('lun_dao', True)])
            bai_ye = all([bai_ye, finished_tasks.get('bai_ye', True)])
        except Exception as e:
            print(f'检查任务失败: {e}')

    all_executor = {

        '论道': (lun_dao_executor, lun_dao),
        '奇袭魔界': (qi_xi_mo_jie_executor, qi_xi_mo_jie),
        '日常抽奖': (ri_chang_chou_jiang_executor, ri_chang_chou_jiang), # 日常抽奖

        '报名': (bao_ming_executor, bao_ming),
        '红包': (hong_bao_executor, hong_bao),
        '小助手': (assistant_executor, assistant),
        '拜谒': (bai_ye_executor, bai_ye),
        '百族供奉': (bai_zu_gong_feng_executor, bai_zu_gong_feng),
        '修炼': (xiu_lian_executor, xiu_lian),

        '混沌灵塔_爬塔': (hun_dun_ling_ta_executor, hun_dun_ling_ta_go_up),
        '混沌灵塔_扫荡': (hun_dun_ling_ta_executor, hun_dun_ling_ta_sao_dang),

        '挑战仙缘': (tiao_zhan_xian_yuan_executor, tiao_zhan_xian_yuan),
        '游历': (youli_executor, youli),
        '双修': (shuangxiu_executor, shuangxiu),
        '灵兽': (ling_shou_executor, ling_shou),
        '副本': (fuben_executor, fuben),
        '坠魔谷': (zhui_mo_gu_executor, zhui_mo_gu),
        
        '兽渊探秘': (shou_yuan_tan_mi_executor, shou_yuan_tan_mi),
        '魔道入侵': (mo_dao_ru_qing_executor, mo_dao_ru_qing),
        '虚天殿': (xu_tian_dian_executor, xu_tian_dian),
        '云梦试剑': (yun_meng_shi_jian_executor, yun_meng_shi_jian),

        '仙盟争霸': (xian_meng_zheng_ba_executor, xian_meng_zheng_ba),

        '爬天梯': (pa_tian_ti_executor, pa_tian_ti),

        '检查日常': (check_ri_chang_executor, check_ri_chang),
    }

    for executor_name, if_execute in all_executor.items():
        executor, if_execute = if_execute
        if if_execute:
            wait_for_evelen()

            start_time = datetime.now()
            try:
                if executor_name in ['论道', '兽渊探秘', '魔道入侵', '虚天殿', '云梦试剑', '仙盟争霸', ]:
                    if datetime.now().hour < 11: #  11点之前不执行
                        print(f'{executor_name}未到执行时间')
                        continue
                
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
                    f.write(f'\n{current_time}-{account_name}-{executor_name}:{e}\n')

            end_time = datetime.now()
            print(f'{executor_name}执行时间: {end_time - start_time}')
            with open('time.txt', 'a', encoding='utf-8') as f:
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
                cost_time = (end_time - start_time).seconds
                f.write(f'\n{current_time}-{account_name}-{executor_name}-执行时间: {cost_time}秒\n')

            executor.go_to_world()

if __name__ == '__main__':
    
    # resolution = (1080, 1920) # (width, height): (554, 984) or (1080, 1920)
    resolution = (720, 1280) # (width, height): (554, 984) or (1080, 1920)
    device_serial = 'emulator-5566' # '都有3'
    # device_serial = 'emulator-5568' # '都有4'
    # device_serial = 'emulator-5570' # '都有5'

    main_region_coords_dt = {
        'emulator-5566': '3087,422,720,1280',
        'emulator-5568': '2351,421,720,1280',
        'emulator-5570': '1612,418,720,1280',
    }

    # 添加环境变量
    # os.environ['RESOLUTION'] = f'{resolution[0]}x{resolution[1]}'
    os.environ['ROOT_DIR'] = f'FanRenXiuXianIcon_{resolution[0]}_{resolution[1]}'
    os.environ['DEVICE_SERIAL'] = device_serial
    os.environ['MAIN_REGION_COORDS'] = main_region_coords_dt[device_serial]

    from utils_adb import get_game_page_coords, wait_for_evelen
    from assistant import AssistantCoordsManager, AssistantExecutor
    from bao_ming import BaoMingCoordsManager, BaoMingExecutor
    from xiu_lian import XiuLianCoordsManager, XiuLianExecutor
    from bai_ye import BaiYeCoordsManager, BaiYeExecutor
    from you_li import YouliCoordsManager, YouLiExecutor
    from fu_ben import FuBenCoordsManager, FuBenExecutor
    from ling_shou import LingShouCoordsManager, LingShouExecutor
    from lun_dao import LunDaoCoordsManager, LunDaoExecutor
    from qi_xi_mo_jie import QiXiMoJieCoordsManager, QiXiMoJieExecutor
    from zhui_mo_gu import ZhuiMoGuCoordsManager, ZhuiMoGuExecutor

    from check_all_tasks import CheckAllTasksCoordsManager, CheckAllTasksExecutor
    from check_ri_chang import CheckRiChangCoordsManager, CheckRiChangExecutor

    from shuang_xiu import ShuangXiuCoordsManager, ShuangXiuExecutor
    from hun_dun_ling_ta import HunDunLingTaCoordsManager, HunDunLingTaExecutor
    from tiao_zhan_xian_yuan import TiaoZhanXianYuanCoordsManager, TiaoZhanXianYuanExecutor
    from pa_tian_ti import PaTianTiCoordsManager, PaTianTiExecutor
    from bai_zu_gong_feng import BaiZuGongFengCoordsManager, BaiZuGongFengExecutor
    from hong_bao import HongBaoCoordsManager, HongBaoExecutor
    from ri_chang_chou_jiang import RiChangChouJiangCoordsManager, RiChangChouJiangExecutor
    from game_control import GameControlCoordsManager, GameControlExecutor

    from shou_yuan_tan_mi import ShouYuanTanMiCoordsManager, ShouYuanTanMiExecutor
    from mo_dao_ru_qing import MoDaoRuQingCoordsManager, MoDaoRuQingExecutor
    from xu_tian_dian import XuTianDianCoordsManager, XuTianDianExecutor
    from yun_meng_shi_jian import YunMengShiJianCoordsManager, YunMengShiJianExecutor

    from xian_meng_zheng_ba import XianMengZhengBaCoordsManager, XianMengZhengBaExecutor

    # main_region_coords = get_game_page_coords(resolution = resolution)
    main_region_coords = tuple(map(int, main_region_coords_dt[device_serial].split(',')))
    # print(f'游戏区域坐标: {main_region_coords}')

    # print("等待60秒, 用于等候定位其他模拟器窗口!")
    # time.sleep(60)

    game_coords_manager = GameControlCoordsManager(main_region_coords, resolution=resolution)

    file_path = os.getenv('game_execute_info_file_path')

    # accounts
    accounts = pd.read_excel(file_path, sheet_name='accounts')

    accounts = accounts[(accounts['execute'] == 1) & (accounts['模拟器'] == device_serial)]
    if len(accounts) == 0:
        print('没有需要执行的账号')
        exit()

    account_name_ls = accounts['account_names'].tolist()
    print(f'需要执行的账号: {account_name_ls}')
    
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

        server = accounts[accounts['account_names'] == account_name]['服务器'].item()
        
        try:
            game_executor = GameControlExecutor(game_coords_manager, account_name=account_name, account=account, server=server)
            game_executor.execute()
        except Exception as e:
            print(f'{account_name}执行失败: {e}')

        daily_task(main_region_coords, account_name=account_name, account_task_info=account_task_info, resolution=resolution, **execute_info)

    # os.system('shutdown -s -t 10') # 关机