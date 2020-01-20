
import requests
import re
import json

url = "https://res.mall.10010.cn/mall/front/js/areaInfo.js"

res = requests.get(url)
json_dict = eval(re.search("[{].*[}]", res.text).group())
print(json_dict['PROVINCE_LIST'])
print(json_dict['PROVINCE_MAP'])
with open("areaInfo.json", 'w') as f:
    json.dump(json_dict, f)