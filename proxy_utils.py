from copy import deepcopy
from telnetlib import Telnet

from utils import *
from queue import Queue
from PyQt5.QtCore import QThread, pyqtSignal
from threading import Thread
import time


def validate_url(url):

    try:
        response = requests.get(url)
        proxy_items = response.text.split()
        return f"校验ip代理成功, 返回{len(proxy_items)}条代理"
    except Exception as e:
        return f"校验ip代理失败"


class ProxyCleaner(QThread):
    cleaned_ip_sender = pyqtSignal(str)  # 把清理好的ip代理发出去
    logging_signal = pyqtSignal(str)  # 用来发日志的信号

    def __init__(self):
        super().__init__()
        self.proxy_url = "http://www.15daili.com/apiProxy.ashx?un=13777893886&pw=5201314.&count=500"    #
        self.proxies = Queue()
        self.proxies_wait = Queue()
        self.proxy_num = 0     # 当前代理池代理ip的数量
        self.thread_num = 20

    def set_ip_url(self, url):
        self.proxy_url = url
        self.logging_signal.emit(f"设置ip代理链接为:{self.proxy_url}")

    def add_proxy(self):

        while True:
            try:
                response = requests.get(self.proxy_url)
                proxy_items = response.text.split()
                for proxy_item in proxy_items:
                    # print("添加待清洗代理:", proxy_item)
                    self.proxies_wait.put(proxy_item)
                return
            except Exception as e:
                self.logging_signal.emit("获取ip代理失败, 请检查ip代理链接是否填写正确")
                time.sleep(10)

    def clean(self):
        while True:
            if self.proxies_wait.empty():
                self.add_proxy()

            proxy = self.proxies_wait.get()
            try:
                hd, port = proxy.split(':')
            except Exception as e:
                print(e, "def clean(self):")
                continue

            try:
                Telnet(hd, port=port, timeout=3)
                self.cleaned_ip_sender.emit(proxy)
                self.add_cleaned_proxy(proxy)

            except Exception as e:
                pass

    def run(self):
        self.logging_signal.emit(f"开启代理清洗")
        for i in range(self.thread_num):
            t = Thread(target=self.clean)
            t.start()

    def get_cleaned_proxy(self):
        proxy = self.proxies.get()      # 获取一个清理好的代理
        self.proxy_num -= 1

        if self.proxy_num > 100:      # 如果ip代理太多了,就清理一下
            self.proxies.queue.clear()
            self.logging_signal.emit("旧的ip代理太多了,清理一下")
            self.proxy_num = 0
        return proxy

    def add_cleaned_proxy(self, proxy):
        self.proxies.put(proxy)      # 添加一个清理好的代理
        self.proxy_num += 1


if __name__ == '__main__':
    proxy_cleaner = ProxyCleaner()
    proxy_cleaner.start()
    while True:
        print("获取到干净的代理:", proxy_cleaner.get_cleaned_proxy())
