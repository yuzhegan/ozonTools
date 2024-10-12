# encoding='utf-8

# @Time: 2024-10-08
# @File: %
#!/usr/bin/env
from icecream import ic
import os
import time
from requests import Request, Session

# daohuo_time = '2024-10-16'  #"2000011333504“ 货到海外仓日期
daohuo_time = '2024-10-23' 
# daohuo_time = None 
# parentOrders = '32279725'
# parentOrders = '32632254'
parentOrders = '33686919'
# parentOrders = '33687036'
# parentOrders = '33687133'


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
response = session.get(
    f'https://seller.ozon.ru/api/supplier-service/companies/current/parent-orders/{parentOrders}',
    headers=headers,
)
# ic(response.json())



#xuanzhe
json_data = {
    'timeslotFromLocal': '2024-10-18T18:00:00',
}

response = session.put(
    f'https://seller.ozon.ru/api/supplier-service/companies/current/parent-orders/{parentOrders}/timeslots',
    # cookies=cookies,
    headers=headers,
    json=json_data,
)
ic(response.status_code)
# ic(response.json())


# if response.status_code == 200:
# tijiao
response = session.get(f'https://seller.ozon.ru/api/supplier-service/companies/current/parent-orders/{parentOrders}/supply-preparation', headers=headers)

ic(response.json())
ic("提交成功")
