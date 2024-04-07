 
import pandas as pd
import sys, os
from pathlib import Path
import requests
import datetime


id = "112"
date = "03-29-2024"
data_string_raw = f"{{'storeId':'{id}','purchaseDate':'{date}'','cardType':'discover','total':'54.14','lastFourDigits':'9996'}}"
print(f"{data_string_raw = }")

def make_receipt_request(data_row):
    card_last_four = '9996'
    sc = data_row["Store Code"]
    td = '05-29-2024' # data_row["Trans. date"].strftime('%Y-%m-%d')
    total = 54.14 #data_row["Amount"]
    data = {
        'storeId': sc,
        'purchaseDate': td,
        'cardType':'discover',
        'total': str(total),
        'lastFourDigits': card_last_four
    }
    # data_raw = f"{{',',}"
    print(data)
    headers = {
    'sec-ch-ua': '"Chromium";v="98", " Not A;Brand";v="99", "Google Chrome";v="98"',
    'accept': 'application/json',
    'Referer': 'https://www.walmart.com/receipt-lookup',
    'content-type': 'application/json',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'sec-ch-ua-platform': '"Mac OS X"'
    }
    
    return requests.post('https://www.walmart.com/chcwebapp/api/receipts', headers=headers, data=data)

def get_in_store_charges(path):
    discover_file_rows_skipped=12
    data=None
    data = pd.read_excel(path, engine="xlrd", skiprows=discover_file_rows_skipped)

    if data.empty:
        return None
    data["Store Code"] = data.Description.str.split(expand=True)[2]
    return data[data['Description'].str.contains("WALMART SC")]    

input_path = Path(sys.argv[1])
try:
    data = get_in_store_charges(input_path)
except Exception as e:
    print(f"Could not parse an Excel file at path {input_path}")
# !!!! TEMPORARY due to large size of sample file
data = data[:10]
# !!!!
print(data)

data.reset_index()
for index, row in data.iterrows():
    print(index, end="\t")
    # print(row)
    response = make_receipt_request(row)
    print(f"{response.content = }")
    exit()

if(False):
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
    --data-raw {data_string_raw}
    --compressed
    '''
    print(f"{request = }")
