# encoding='utf-8
# @Time: 2024-10-12
# @File: %
#!/usr/bin/env
from icecream import ic
import os
from requests import request, Session

from genparentorders import genparentorders
import random

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-Hans',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'cookie': '__Secure-ab-group=23; __Secure-ext_xcid=c8446847cd6bc19d04b0fddaeac083a1; __Secure-user-id=153179496; bacntid=3741873; contentId=1654428; xcid=167a550920405197333de4d4b684ab68; sc_company_id=1654428; x-o3-language=zh-Hans; abt_data=7.ZG9NzLBNo11ljVT6IlsvP2wBrL5gpGqsScmMYLmah6a85MMNawlkjfYqDuzLpJSBS590qlRmMtwwr9TYP_7b4iwGH1ZXmjHP-DHbM5H9ivqzbKfF4gAK9ZDfSd-ofRHzrwkPOefv_zsXujycJ2vmHS3lnqXqwq37e8UnWbWGRbsHpct6w4GakEoeSqE8ffbx6Ic-2wXtTShfwxnK2QesFqEW2fx7XmzeA-j2xR6BGRuKckd6SGubn_hnEgMr_g5xlNPA_MjMb6gPgVpWW9KIV5xK_JFPMLF03aRSNhvoYKNNa-u7wFAKhh7giCSgX5M4nDiOidCT7tsqPJYPRb6a7gxjGo5CkvQXuILmTnK4E07nkwcLKMGx0cdQAMOqigtD9KIBcuwp91h6K06lxFu8z2XBjkiRZ1k-fI-5PeVpaJ0slh1mM7rXdw5-r_N9Ej52aLHc_FsIR2a85IOM6uf_nTrPti_AXA-ND8Yp12NG5C4elMGNv3irtkfhIdiBnb5uha1-5OVGSP6gSrJdm7g; abt_data=7.6WVN9TUz5VhxRXyyS4nxQWnZK7Tf4P4HJGfQ8kKxz5eZkXyLE7QeW_rlyeElgZBzrPCotNFXcl3yDo0qWVPhM5yjb-MQ9B3WoOWn332KT1Fho__YJLHQ7_OlVdT6-xpaNGabckPYchYYutccoevCgLQPL06m3EPIkyLxUdeA8WbCKptN10kaxcW4AOo2VgrH_sy7IUIVkv9UWj18vHTxkp7EXTEX5YH04Yc4w5T0v38V3rCPyud-VI-Dwzs33V9nwwcd88FiAfYFuAUEI6dS7noxs3RKoMa87X-cyggEsVUNUDdqpsaebyTwf9FxWMlBo8rCGpZLrBsUPMQO7N6nYIbJJTqb0eZ5J0yb_EY3A0-jY_0O0t-bJXBhw7jFyYvwb9z_PGpB7VQSnjypRoLEiLDz4ldvq-wsXywQf-JYE_JQYBgZGzPbeEFvkxWgIDPel_JAnVxecDIRBH59Dib6VPLJK9GgXNxxIz225yH53hZPEegmbBDgANMkPTNQcj_yR5I0gt1TgyErgV8qYbsChMUL; __Secure-ETC=fb21c95e94ae6b491ae28a1fcdbccae5; __Secure-refresh-token=6.153179496.FMgxpNZZRJS_FJc9AvaajA.23.AZhGH_KPQKugyHd_a4spOlLy0-wvqAZ75nAUMVfc41r5MTBjE3ZAiMxgGxquH1LeGak32dvwG3N1oNOjZNWZx1M.20240115055703.20241012114515.QLOBFvi7Ol3_bE-Lb9bxoFJDDydg5RL2L595oYndW9A.13ea33e4ea339c3ab; __Secure-access-token=6.153179496.FMgxpNZZRJS_FJc9AvaajA.23.AZhGH_KPQKugyHd_a4spOlLy0-wvqAZ75nAUMVfc41r5MTBjE3ZAiMxgGxquH1LeGak32dvwG3N1oNOjZNWZx1M.20240115055703.20241012114515.wvKRfep2QAE43Gr3nrq2vwrfvskqpwMHb8VD9nF-kiY.1b1049ace1f54188c',
    'origin': 'https://seller.ozon.ru',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://seller.ozon.ru/app/supply/orders?filter=SupplyPreparation',
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
shippmentno = '2000011912742'
parentOrders = genparentorders(session, shippmentno)


data = '{"timeslotFromLocal":"2024-10-18T18:00:00"}'

response = session.put(f'https://seller.ozon.ru/api/supplier-service/companies/current/parent-orders/{parentOrders}/timeslots', headers=headers, data=data)
ic(response.status_code)
