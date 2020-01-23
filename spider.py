from datetime import datetime

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
    logging_signal = pyqtSignal(str)  # 用来发日志的信号

    def __init__(self):
        super().__init__()
        # 定义一些信号
        self.has_been_started = False
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
        self.open_multistage_scheduling = False  # 开启多级调度算法
        self.scheduling_hash_table = dict()  # 用于进行调度的哈希表
        self.scheduling_stage_num = 3  # 3级调度

        # 添加任务
        # self.add_task()

    def set_custom_rules(self, rules):
        self.custom_rules.clear()  # 先清空原有的规则
        for rule in rules:
            self.logging_signal.emit("接收到自定义规则:" + rule)
            self.custom_rules.append(rule)
        if len(rules) == 0:
            self.logging_signal.emit("关闭自定义规则")

    def remove_all_task(self):
        while not self.q.empty():
            task = self.q.get()
            self.logging_signal.emit("清除任务:" + str(task))

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
        self.logging_signal.emit("爬虫接收到了任务:" + str(task))
        self.q.put(task)

    def dispatcher(self):
        while True:
            task = self.q.get()
            self.q.put(task)

            # 如果进行多级调度的话
            if self.open_multistage_scheduling:
                hash_key = task['provinceName'] + task['cityName']  # 用省名+城市名进行哈希作为key
                if hash_key not in self.scheduling_hash_table:
                    self.scheduling_hash_table[hash_key] = 0  # 0代表最优先的级别
                current_stage = self.scheduling_hash_table[hash_key]
                # 如果这个不是最优先的,先往后稍稍
                if current_stage > 0:
                    # print(f"跳过{task['provinceName']} {task['cityName']}, 其调度等级为:{current_stage}")
                    self.scheduling_hash_table[hash_key] = (current_stage + 1) % self.scheduling_stage_num
                    continue
            yield task

    def crawl_numbers(self):

        while True:
            while self.is_suspend:  # 如果现在暂停的话
                time.sleep(3)  # 就休息一下

            task = next(self.dispatcher())

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
                                        params=params, cookies=self.cookies, proxies={'https': 'https://' + proxy},
                                        timeout=3)
                # print(response.raw._original_response.fp.raw._sock.getpeername())
                num_list = re.findall("1\\d{10}", response.text)
                for num in num_list:
                    # self.phone_numbers.add(num)
                    self.send_data(num, task['provinceName'], task['cityName'])
                # 把能用的代理重新添加回去
                if self.proxy_cleaner.proxy_num < 50:
                    self.proxy_cleaner.add_cleaned_proxy(proxy)
                # print(task, datetime.now().strftime('%m-%d %H:%M:%S'), len(num_list))
                time.sleep(0.2)
                if self.open_multistage_scheduling:
                    self.update_hash_table(task, len(num_list))  # 更新用于调度的哈希表

            except Exception as e:
                pass

    def update_hash_table(self, task, num_count):
        """

        :param task: 包含 provinceCode, cityCode, provinceName, cityName
        :param num_count:
        :return:
        """
        hash_key = task['provinceName'] + task['cityName']  # 用省名+城市名进行哈希作为key
        current_stage = self.scheduling_hash_table[hash_key]
        # 现在有了之前的调度等级, 如果这次返回的号码数量是0个, 把这个省市降一个等级
        if num_count == 0:
            current_stage = (current_stage + 1) % self.scheduling_stage_num

        # 更新调度等级
        self.scheduling_hash_table[hash_key] = current_stage

    def send_data(self, num, province, city):
        type_of_card, match_index_dict = classify_num(num, self.custom_rules)
        self.sender.emit(num, province, city, type_of_card, match_index_dict)

    def suspend(self):
        self.is_suspend = True
        self.logging_signal.emit("爬虫暂停")

    def carry_on(self):
        self.is_suspend = False

        if self.has_been_started:
            self.logging_signal.emit("爬虫继续进行爬取")
        # 如果是第一次启动
        else:
            self.has_been_started = True
            self.start()

    def run(self):
        # self.logging_signal.emit("联系QQ: 1158677160, 微信: lly19980726")
        self.logging_signal.emit("爬虫首次启动")
        self.logging_signal.emit(f"爬虫线程数:{self.thread_num}")
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
