# Class_scan_host.py

__doc__ = """
扫描存活的主机
输入的可以是
一个 A/B/C类地址
"""
from mysite.tools.Class_scan_ip import scan_ip
import re
import time

class scan_host(object):
    def __init__(self, hostlist, port):
        self.hostlist = hostlist
        self.port = port
        self.isrun = True
    def check_data(self):
        if "/" in self.hostlist:
            type_ip = self.hostlist.split("/")[-1]
            try:
                type_ip = int(type_ip)
            except:
                print("数据错误")
                return False
            if not type_ip in (8,16,24):
                print("error")
                return
            ip = self.hostlist.split("/")[0]
            if not re.match(r"(([1-9]?\d|1\d{2}|2[0-4]\d|25[0-5])\.){3}([1-9]?\d|1\d{2}|2[0-4]\d|25[0-5])", ip):
                print("ip地址错误")
                return False
        else:
            print("数据错误")
            return False
        self.ip = ip
        self.type_ip = type_ip
        return (ip, type_ip)
    def scan(self):
        print("asd")
        if not self.check_data():
            return
        ips = self.ip.split(".")
        if self.type_ip == 24:
            ips.pop()
            self.send = scan_ip(1, 0, "wlan0", ".".join(ips), self.port)
            self.send.start()
        if self.type_ip == 16:
            ips = self.ip.split(".")
            ips.pop()
            ips.pop()
            self.scan_16(ips)
        if self.type_ip == 8:
            ips = self.ip.split(".")
            ips.pop()
            ips.pop()
            ips.pop()
            self.scan_8(ips)
        print("end")
    def scan_16(self, ips):
        print(".".join(ips))
        for i in range(1, 256):
            self.send = scan_ip(1, 0, "wlan0", ".".join(ips) + "." + str(i), self.port)
            self.send.start()
            time.sleep(0.5)
        self.isrun = False
    def scan_8(self, ips):
        for i in range(1, 256):
            ips_othor = ips.copy()
            ips_othor.append(str(i))
            self.scan_16(ips_othor)

if __name__ == '__main__':
    test = scan_host("203.66.65.94/16", "80")
    test.scan()
