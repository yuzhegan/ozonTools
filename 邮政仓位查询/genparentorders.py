# encoding='utf-8
# @Time: 2024-10-11
# @File: %
#!/usr/bin/env
from icecream import ic
import os
import requests
import requests
url = 'https://seller.ozon.ru/api/supplier-service/companies/current/parent-orders'
def genparentorders(session, parentOrderNumber):
    params={
      "marketplaceCompanyId": "1654428",
      "orderNumber": "",
      "pageNumber": "1",
      "pageSize": "20",
      "isSortingDesc": "true",
      "statesGroup": "SupplyPreparation",
      "sortingKey": "CreationDate"
    }
    # 发送GET请求
    response = session.get(url, params=params).json()
    # ic(response)
    genparentorders = response['parentOrders']
    for parentorder in genparentorders:
        if str(parentorder['parentOrderNumber']) == str(parentOrderNumber):
            ic(parentorder['parentOrderId'])
            ic(parentorder['parentOrderNumber'])
            return str(parentorder['parentOrderId'])

