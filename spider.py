import requests
import json
from queue import Queue
from threading import Thread
import re

from PyQt5.QtCore import QThread, pyqtSignal

from utils import classify_num
import time
import random
from proxy_utils import ProxyCleaner


class Spider(QThread):
    sender = pyqtSignal(str, str, str, list, dict)  # 把号码发出去

    def __init__(self):
        super().__init__()
        # 定义一些信号
        self.thread_num = 100
        self.is_suspend = False
        self.phone_numbers = set()
        self.proxy_cleaner = ProxyCleaner()
        self.custom_rules = list()
        self.q = Queue()
        self.cookies = {
            'UID': 'MKkUnB7tp7d5Lr3cmNXuu5l2uWvECW3F',
            'SHOP_PROV_CITY': '',
            'tianjincity': '11|110',
            'tianjin_ip': '0',
            'mallcity': '11|110',
            'gipgeo': '11|110',
        }
        self.headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
            'Referer': 'https://msgo.10010.com/newMsg/onLineGo/html/fill.html?sceneFlag=03&goodsId=981610241535&productName=%E5%A4%A7%E7%8E%8B%E5%8D%A1&channel=9999&p=51&c=558&u=rSqV6hmVlPRu8PHYYIjcUQ==&s=02,03&sceneFlag=03',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
        }
        # 添加任务
        # self.add_task()

    def set_custom_rules(self, rules):
        self.custom_rules.clear()     # 先清空原有的规则
        for rule in rules:
            print("接收到自定义规则:", rule)
            self.custom_rules.append(rule)

    def remove_all_task(self):
        while not self.q.empty():
            task = self.q.get()
            print("清除任务:", task)

    def add_task(self):
        url = "https://m.10010.com/king/kingNumCard/init?product=0&channel=611&WT.mc_id=jituan_wangka_1803_baidusem_401e66b6329c53dd&utm_source=baidusem&utm_medium=cpc&utm_content=textlink&utm_campaign=jituan_wangka_1803_baidusem_401e66b6329c53dd&bd_vid=11434467437403140638"
        response = requests.get(url)
        json_dict = json.loads(response.text)

        province_dict = dict()
        for province in json_dict["provinceData"]:
            province_name = province["PROVINCE_NAME"]
            provinceCode = province["PROVINCE_CODE"]
            province_dict[provinceCode] = province_name

        print(province_dict.values())
        #     province_pro_order_number = province["PRO_ORDER_NUMBER"]
        #     print(province_name, provinceCode, province_pro_order_number)

        # for provinceCode, groupKey in json_dict["proGroupNum"].items():
        #     print(provinceCode, groupKey)

        for provinceCode, cities in json_dict["cityData"].items():
            print(province_dict[provinceCode], ":", cities)
            for city in cities:
                cityCode = city["CITY_CODE"]
                groupKey = json_dict["proGroupNum"][provinceCode]
                cityName = city["CITY_NAME"]
                print(provinceCode, cityCode, groupKey, cityName)
                self.q.put({"provinceCode": provinceCode, "cityCode": cityCode, "groupKey": groupKey,
                            "cityName": cityName, "provinceName": province_dict[provinceCode]})

    def is_task_empty(self):
        return self.q.empty()

    def add_single_task(self, task):
        print("爬虫接收到了任务:", task)
        self.q.put(task)

    def crawl_numbers(self):

        while not self.q.empty():
            while self.is_suspend:     # 如果现在暂停的话
                time.sleep(3)          # 就休息一下
            task = self.q.get()
            self.q.put(task)

            params = (
                ('callback', 'jsonp_queryMoreNums'),
                ('provinceCode', task['provinceCode']),
                ('cityCode', task['cityCode']),
                ('monthFeeLimit', '0'),
                ('goodsId', '181610241535'),
                ('searchCategory', '3'),
                ('net', '01'),
                ('amounts', '200'),
                ('codeTypeCode', ''),
                ('searchValue', ''),
                ('qryType', '02'),
                ('goodsNet', '4'),
                ('channel', 'msg-xsg'),
                ('_', str(int(time.time() * 1000))),  # 时间戳
            )

            proxy = self.proxy_cleaner.get_cleaned_proxy()
            try:
                response = requests.get('https://msgo.10010.com/NumApp/NumberCenter/qryNum', headers=self.headers,
                                        params=params, cookies=self.cookies, proxies={'https': 'https://' + proxy})
                #
                for num in re.findall("1\\d{10}", response.text):
                    self.phone_numbers.add(num)
                    self.send_data(num, task['provinceName'], task['cityName'])
                # 把能用的代理重新添加回去
                self.proxy_cleaner.add_cleaned_proxy(proxy)

            except Exception as e:
                pass
                # print("def crawl_numbers(self):", e)

    def send_data(self, num, province, city):
        type_of_card, match_index_dict = classify_num(num, self.custom_rules)
        if len(type_of_card):
            self.sender.emit(num, province, city, type_of_card, match_index_dict)

    def suspend(self):
        self.is_suspend = True
        print("暂停")

    def carry_on(self):
        if self.is_suspend is True:
            self.is_suspend = False
            print("重新进行爬取")
        # 如果是第一次启动
        else:
            print("首次启动")
            self.start()

    def run(self):
        print("联系QQ: 1158677160")
        self.proxy_cleaner.start()

        ths = []
        for i in range(self.thread_num):
            th = Thread(target=self.crawl_numbers)
            th.start()
            ths.append(th)

        for th in ths:
            th.join()


if __name__ == '__main__':
    spider = Spider()

    print('finish add task')
    spider.run()
