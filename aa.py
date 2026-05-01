import hashlib


import requests

url = "http://zj.baiyikj.cn/etcThirdPark/payRequest"
playload={
  "appId": "byffd22b27b94d",
  "billCode": "61200000062026043015491051",
  "inChannelId": "52",
  "inTime": "2026-04-30 15:48:58",
  "nonceStr": "3cde632b8d824cf1976b474a86007320",
  "orderId": "29",
  "outChannelId": "4",
  "outTime": "2026-04-30 15:49:10",
  "parkId": "6120000006",
  "parkName": "西安高新华府停车场",
  "payAmount": "1",
  "plate": "陕AD93375",
  "plateColor": "1",
  "timestamp": "1777535350027",
  "totalAmount": "1"
}
import datetime
playload["timestamp"] = str(int(datetime.datetime.now().timestamp() * 1000))
# 按 key 排序后拼接
sorted_items = sorted(playload.items())
result = '&'.join([f"{k}={v}" for k, v in sorted_items])
result += "&secret=b69dba6a550165c7e4d1bdf35e77dfa6"
print(result)


md5_utf8 = hashlib.md5(result.encode('utf-8')).hexdigest()
print("md5:",md5_utf8.upper())

playload["sign"] = md5_utf8.upper()
response = requests.post(url, json=playload)
print(response.text)