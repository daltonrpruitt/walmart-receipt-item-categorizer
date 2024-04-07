 

id = "112"
date = "03-29-2024"
data_raw = f"\{'storeId':'{id}','purchaseDate':'{date}'','cardType':'discover','total':'54.14','lastFourDigits':'9996'\}"
print(f"{data_raw = }")

# echo "${data_raw}"
request = f'''
curl 'https://www.walmart.com/chcwebapp/api/receipts'
  -H 'sec-ch-ua: "Chromium";v="98", " Not A;Brand";v="99", "Google Chrome";v="98"'
  -H 'accept: application/json'
  -H 'Referer: https://www.walmart.com/receipt-lookup'
  -H 'content-type: application/json'
  -H 'sec-ch-ua-mobile: ?0'
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
  -H 'sec-ch-ua-platform: "Mac OS X"'
  --data-raw {data_raw}
  --compressed
'''
print(f"{request = }")
