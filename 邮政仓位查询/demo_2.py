# encoding='utf-8

# @Time: 2024-10-08
# @File: %
#!/usr/bin/env
from icecream import ic
import os
import time
from requests import Request, Session
import random
from genparentorders import genparentorders




headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-Hans',
    'cookie': '__Secure-ab-group=23; __Secure-ext_xcid=c8446847cd6bc19d04b0fddaeac083a1; __Secure-user-id=153179496; bacntid=3741873; contentId=1654428; xcid=167a550920405197333de4d4b684ab68; sc_company_id=1654428; x-o3-language=zh-Hans; __Secure-ETC=38eba657574d9bc700ea857909a3f9ce; rfuid=NjkyNDcyNDUyLDEyNC4wNDM0NzUyNzUxNjA3NCwxMDI4MjM3MjIzLC0xLC05ODc0NjQ3MjQsVzNzaWJtRnRaU0k2SWxCRVJpQldhV1YzWlhJaUxDSmtaWE5qY21sd2RHbHZiaUk2SWxCdmNuUmhZbXhsSUVSdlkzVnRaVzUwSUVadmNtMWhkQ0lzSW0xcGJXVlVlWEJsY3lJNlczc2lkSGx3WlNJNkltRndjR3hwWTJGMGFXOXVMM0JrWmlJc0luTjFabVpwZUdWeklqb2ljR1JtSW4wc2V5SjBlWEJsSWpvaWRHVjRkQzl3WkdZaUxDSnpkV1ptYVhobGN5STZJbkJrWmlKOVhYMHNleUp1WVcxbElqb2lRMmh5YjIxbElGQkVSaUJXYVdWM1pYSWlMQ0prWlhOamNtbHdkR2x2YmlJNklsQnZjblJoWW14bElFUnZZM1Z0Wlc1MElFWnZjbTFoZENJc0ltMXBiV1ZVZVhCbGN5STZXM3NpZEhsd1pTSTZJbUZ3Y0d4cFkyRjBhVzl1TDNCa1ppSXNJbk4xWm1acGVHVnpJam9pY0dSbUluMHNleUowZVhCbElqb2lkR1Y0ZEM5d1pHWWlMQ0p6ZFdabWFYaGxjeUk2SW5Ca1ppSjlYWDBzZXlKdVlXMWxJam9pUTJoeWIyMXBkVzBnVUVSR0lGWnBaWGRsY2lJc0ltUmxjMk55YVhCMGFXOXVJam9pVUc5eWRHRmliR1VnUkc5amRXMWxiblFnUm05eWJXRjBJaXdpYldsdFpWUjVjR1Z6SWpwYmV5SjBlWEJsSWpvaVlYQndiR2xqWVhScGIyNHZjR1JtSWl3aWMzVm1abWw0WlhNaU9pSndaR1lpZlN4N0luUjVjR1VpT2lKMFpYaDBMM0JrWmlJc0luTjFabVpwZUdWeklqb2ljR1JtSW4xZGZTeDdJbTVoYldVaU9pSk5hV055YjNOdlpuUWdSV1JuWlNCUVJFWWdWbWxsZDJWeUlpd2laR1Z6WTNKcGNIUnBiMjRpT2lKUWIzSjBZV0pzWlNCRWIyTjFiV1Z1ZENCR2IzSnRZWFFpTENKdGFXMWxWSGx3WlhNaU9sdDdJblI1Y0dVaU9pSmhjSEJzYVdOaGRHbHZiaTl3WkdZaUxDSnpkV1ptYVhobGN5STZJbkJrWmlKOUxIc2lkSGx3WlNJNkluUmxlSFF2Y0dSbUlpd2ljM1ZtWm1sNFpYTWlPaUp3WkdZaWZWMTlMSHNpYm1GdFpTSTZJbGRsWWt0cGRDQmlkV2xzZEMxcGJpQlFSRVlpTENKa1pYTmpjbWx3ZEdsdmJpSTZJbEJ2Y25SaFlteGxJRVJ2WTNWdFpXNTBJRVp2Y20xaGRDSXNJbTFwYldWVWVYQmxjeUk2VzNzaWRIbHdaU0k2SW1Gd2NHeHBZMkYwYVc5dUwzQmtaaUlzSW5OMVptWnBlR1Z6SWpvaWNHUm1JbjBzZXlKMGVYQmxJam9pZEdWNGRDOXdaR1lpTENKemRXWm1hWGhsY3lJNkluQmtaaUo5WFgxZCxXeUo2YUMxRFRpSmQsMCwxLDAsMjQsMjM3NDE1OTMwLDgsMjI3MTI2NTIwLDAsMSwwLC00OTEyNzU1MjMsUjI5dloyeGxJRWx1WXk0Z1RtVjBjMk5oY0dVZ1IyVmphMjhnVjJsdU16SWdOUzR3SUNoWGFXNWtiM2R6SUU1VUlERXdMakE3SUZkcGJqWTBPeUI0TmpRcElFRndjR3hsVjJWaVMybDBMelV6Tnk0ek5pQW9TMGhVVFV3c0lHeHBhMlVnUjJWamEyOHBJRU5vY205dFpTOHhNamN1TUM0d0xqQWdVMkZtWVhKcEx6VXpOeTR6TmlBeU1EQXpNREV3TnlCTmIzcHBiR3hoLGV5SmphSEp2YldVaU9uc2lZWEJ3SWpwN0ltbHpTVzV6ZEdGc2JHVmtJanBtWVd4elpTd2lTVzV6ZEdGc2JGTjBZWFJsSWpwN0lrUkpVMEZDVEVWRUlqb2laR2x6WVdKc1pXUWlMQ0pKVGxOVVFVeE1SVVFpT2lKcGJuTjBZV3hzWldRaUxDSk9UMVJmU1U1VFZFRk1URVZFSWpvaWJtOTBYMmx1YzNSaGJHeGxaQ0o5TENKU2RXNXVhVzVuVTNSaGRHVWlPbnNpUTBGT1RrOVVYMUpWVGlJNkltTmhibTV2ZEY5eWRXNGlMQ0pTUlVGRVdWOVVUMTlTVlU0aU9pSnlaV0ZrZVY5MGIxOXlkVzRpTENKU1ZVNU9TVTVISWpvaWNuVnVibWx1WnlKOWZYMTksNjUsLTExODM0MTA3MiwxLDEsLTEsMTY5OTk1NDg4NywxNjk5OTU0ODg3LDMzNjAwNzkzMywxNg==; abt_data=7.xF46voYrDDKS3Wvoh1SwiMwrH3nUjRKMJcHFrv1-10cp9U4xIR7pUvHtnsAfZjaNbRwlk1zYXOJ69zRg1n-FvD3MNemUUCmOByBg-DmnnE2FL0rqY5YcoJSvX19aNaCNrJuBxBfzKCGinpyr-B-tT_3wkN4zV6qeCipdpaYE8xVLFYLJ2AwNORVRCwWKFiJSyeoV9WxNJi2Y0B9-EET9U5g8OB-5KtlZ8aClb9EpQgXLAfRGJzItfCFFGWzEx1dZQD0Dt928AAh4Gz31X7yBdv9pM7bBl44n78SdMdaReXX6myPiwbao36u0TYT7VPcrp3AseQMa8mQGRkuoEaMul4uRIQAoheqN0x56-vztFQIvsiW9823lEhgGpn3oe5i3dvu50kRzWnK9C5Y0aSouQHLNt233eKaEJKRytF6IhOIsH2_LjDN-Q0H54LrhxAsSgR5SLD9zOhsIQ-z0hNzW66Aa6PjAQyCrgWST7ig5i2_0XIRHjgrS4I0; __Secure-access-token=6.153179496.FMgxpNZZRJS_FJc9AvaajA.23.AXvZ8T1AIl-AvzQuMmSqbVPNGGyyN0bmagAJE5j24oozweJ9QNOZQa3nZX08L-QDFfu2BzmFOahmFDw0EF5e8jc.20240115055703.20241008075350.AHBL3CxYjZ5VhvRiishdWzBZYI_uBZFZd0Roq3QJowI.12172b36c18b50051; __Secure-refresh-token=6.153179496.FMgxpNZZRJS_FJc9AvaajA.23.AXvZ8T1AIl-AvzQuMmSqbVPNGGyyN0bmagAJE5j24oozweJ9QNOZQa3nZX08L-QDFfu2BzmFOahmFDw0EF5e8jc.20240115055703.20241008075350.n0hkypyH5LupLVfeVrwuybyRS7w80UJertfG_0JmIWw.1893ec98800576eb2; abt_data=7.ZG9NzLBNo11ljVT6IlsvP2wBrL5gpGqsScmMYLmah6a85MMNawlkjfYqDuzLpJSBS590qlRmMtwwr9TYP_7b4iwGH1ZXmjHP-DHbM5H9ivqzbKfF4gAK9ZDfSd-ofRHzrwkPOefv_zsXujycJ2vmHS3lnqXqwq37e8UnWbWGRbsHpct6w4GakEoeSqE8ffbx6Ic-2wXtTShfwxnK2QesFqEW2fx7XmzeA-j2xR6BGRuKckd6SGubn_hnEgMr_g5xlNPA_MjMb6gPgVpWW9KIV5xK_JFPMLF03aRSNhvoYKNNa-u7wFAKhh7giCSgX5M4nDiOidCT7tsqPJYPRb6a7gxjGo5CkvQXuILmTnK4E07nkwcLKMGx0cdQAMOqigtD9KIBcuwp91h6K06lxFu8z2XBjkiRZ1k-fI-5PeVpaJ0slh1mM7rXdw5-r_N9Ej52aLHc_FsIR2a85IOM6uf_nTrPti_AXA-ND8Yp12NG5C4elMGNv3irtkfhIdiBnb5uha1-5OVGSP6gSrJdm7g',
    'priority': 'u=1, i',
    # 'referer': 'https://seller.ozon.ru/app/supply/orders/32633291',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'x-o3-company-id': '1654428',
    'x-o3-language': 'zh-Hans',
}



session = Session()
session.headers.update(headers)



daohuo_time = '2024-10-12'  #"2000011333504“ 货到海外仓日期
shippmentno = '2000011332950'
# daohuo_time = None 
# parentOrders = '32632254'
parentOrders = genparentorders(session, shippmentno)
# parentOrders = '32665708'










response = session.get(
    f'https://seller.ozon.ru/api/supplier-service/companies/current/parent-orders/{parentOrders}',
    headers=headers,
)
yuye_time = response.json()['timeslot']['fromLocal'] # "2024-10-19T10:00:00"  #当前预约时间
ic(yuye_time)

str_today = time.strftime("%Y-%m-%d", time.localtime())

from datetime import datetime, timedelta



while True:
    time.sleep(random.randint(50, 80))

    # 计算 lastDayWithTimeslots
    parent_order_date = datetime.strptime(daohuo_time, "%Y-%m-%d")
    today_date = datetime.strptime(str_today, "%Y-%m-%d")
    days_difference = (parent_order_date - today_date).days
    ic(days_difference)
    if daohuo_time and days_difference > 7:
        lastDayWithTimeslot = (today_date + timedelta(days=min(days_difference, 7)) + timedelta(1))
        lastDayWithTimeslots = lastDayWithTimeslot.strftime("%Y-%m-%d")
        params = (
            ('lastDayWithTimeslots', lastDayWithTimeslots),
        )
            # chaxun
        try:
            response = session.get(f'https://seller.ozon.ru/api/supplier-service/companies/current/parent-orders/{parentOrders}/timeslots', headers=headers, params=params)
            ic(lastDayWithTimeslots)  # 添加这行来查看计算出的 lastDayWithTimeslots 值
        except Exception as e:
            ic(e)
            continue
    else:
        try:
            response = session.get(f'https://seller.ozon.ru/api/supplier-service/companies/current/parent-orders/{parentOrders}/timeslots', headers=headers)
        except Exception as e:
            ic(e)
            continue
    
    # 找到第一个不是周末的日期
    index = 0
    while True:
        if daohuo_time:
            first_day = response.json()['days'][index]['date']
            first_day_date = datetime.strptime(first_day, "%Y-%m-%d").date()
            ic(first_day_date)
            if (first_day_date.weekday() not in [5, 6]) and (first_day_date >= parent_order_date.date()):  # 不是周六或周日 且要大于到货时间
                break
            index += 1
        else:
            first_day = response.json()['days'][index]['date']
            first_day_date = datetime.strptime(first_day, "%Y-%m-%d").date()
            ic(first_day_date)
            if first_day_date.weekday() not in [5, 6]:
                break
            index += 1
    
    ic(first_day)
    
    # exit()
    first_day_date = datetime.strptime(first_day, "%Y-%m-%d").date()
    yuyue_time_date = datetime.strptime(yuye_time[:10], "%Y-%m-%d").date()
    daohuo_time_date = datetime.strptime(daohuo_time, "%Y-%m-%d").date()
    ic(first_day_date, yuyue_time_date, daohuo_time_date)
    
    # 检查first_day是否为周六或周日
    is_weekend = first_day_date.weekday() in [5, 6]  # 5是周六，6是周日 邮政周末不上班
    ic(is_weekend)
    avaliable_timelist = ['02:00:00', '03:00:00', '04:00:00', '05:00:00', '06:00:00', '07:00:00', '08:00:00', '09:00:00', '10:00:00', '11:00:00', '12:00:00', '13:00:00', '14:00:00', '15:00:00', '16:00:00', '17:00:00', '18:00:00', '19:00:00', '20:00:00', '21:00:00', '22:00:00', '23:00:00']  # 邮政可配送时间段
    
    if daohuo_time_date <= first_day_date < yuyue_time_date and not is_weekend:
        # print("first_day 在 daohuo_time 和 yuyue_time 之间，且不是周末")
        index2 = 0 
        while True:
            time.sleep(random.randint(2, 5))
            ic(index2)
            fromLocal_times = response.json()['days'][index2]['timeslots']
            # ic(fromLocal_times)
            # fromLocal_time = response.json()['days'][0]['timeslots'][0]['fromLocal'] # "2024-10-19T10:00:00"
            fromLocal_day = fromLocal_times[0]['fromLocal'].split('T')[0]
            ic(fromLocal_day)
            ic(first_day)
            if datetime.strptime(fromLocal_day, "%Y-%m-%d").date() == datetime.strptime(first_day, "%Y-%m-%d").date(): # 判断日期是否相等
                # break

                for fromLocal_time in fromLocal_times:
                #判断 日期是否在指定日期范围内
                # ic("进入挑选时间段")
                    choose_time = fromLocal_time['fromLocal'].split('T')[1]
                    ic(choose_time)
                    if choose_time in avaliable_timelist:
                        ic(fromLocal_time['fromLocal'])
                        json_data = {
                            'timeslotFromLocal': fromLocal_time['fromLocal'],
                        }
                        response1 = session.put(
                            f'https://seller.ozon.ru/api/supplier-service/companies/current/parent-orders/{parentOrders}/timeslots',
                            headers=headers,
                            json=json_data,
                        )
                        ic(response.status_code)
                        if response1.status_code == 200:
                            # 提交
                            response1 = session.get(f'https://seller.ozon.ru/api/supplier-service/companies/current/parent-orders/[parentOrders]/supply-preparation', headers=headers)
                            ic(response1.json())
                            ic("提交成功")
                            response = session.get(
                                f'https://seller.ozon.ru/api/supplier-service/companies/current/parent-orders/{parentOrders}',
                                headers=headers,
                            )
                            yuye_time = response.json()['timeslot']['fromLocal'] # "2024-10-19T10:00:00"  #当前预约时间
                            ic(yuye_time)
                            break
                    else:
                        print("fromLocal_time 不满足条件（不在指定时间范围内）")
                break
            
            index2 += 1
            break

    else:
        print("first_day 不满足条件（不在指定日期范围内或是周末）")




# #xuanzhe
# json_data = {
#     'timeslotFromLocal': '2024-10-23T11:00:00',
# }
#
# response = session.put(
#     'https://seller.ozon.ru/api/supplier-service/companies/current/parent-orders/32633291/timeslots',
#     # cookies=cookies,
#     headers=headers,
#     json=json_data,
# )
# ic(response.status_code)
#
#
# if response.status_code == 200:
#     #tijiao
#     response = session.get('https://seller.ozon.ru/api/supplier-service/companies/current/parent-orders/32633291/supply-preparation', headers=headers)
#
#     ic(response.json())
