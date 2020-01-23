import requests


def sendBuyRequest(essProvince, essCity, number, goodsId, webProvince, webCity, webCounty, address, certName, certId, contractPhone):
    print("-"*100)
    print('\n'.join([essProvince, essCity, number, goodsId, webProvince, webCity, webCounty, address, certName, certId, contractPhone]))
    print("-" * 100)

    cookies = {
        'UID': 'MKkUnB7tp7d5Lr3cmNXuu5l2uWvECW3F',
        'tianjincity': '11|110',
        'tianjin_ip': '0',
        'mallcity': '11|110',
        'gipgeo': '11|110',
        'SHOP_PROV_CITY': '',
    }

    headers = {
        'Origin': 'https://msgo.10010.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Referer': 'https://msgo.10010.com/newMsg/onLineGo/html/fill.html?sceneFlag=03&goodsId=981702278573&productName=%E5%A4%A9%E7%8E%8B%E5%8D%A1&channel=9999&p=51&c=558&u=rSqV6hmVlPRu8PHYYIjcUQ==&s=02,03&sceneFlag=03',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
    }

    data = r'{"numInfo":{"essProvince":"%s","essCity":"%s","number":"%s"},"goodInfo":{"goodsId":"%s","sceneFlag":"03"},"postInfo":{"webProvince":"%s","webCity":"%s","webCounty":"%s","address":"%s"},"certInfo":{"certTypeCode":"02","certName":"%s","certId":"%s","contractPhone":"%s"},"u":"rSqV6hmVlPRu8PHYYIjcUQ==","channel":"9999","marketingStatus":"0"}' \
           % (essProvince, essCity, number, goodsId, webProvince, webCity, webCounty, address, certName, certId, contractPhone)
    print(data)
    response = requests.post('https://msgo.10010.com/scene-buy/scene/buy', headers=headers, cookies=cookies,
                             data=data.encode('utf-8'))
    print(response.text)
    return response.text
