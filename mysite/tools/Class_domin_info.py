
__version__ = "SearchAPP_v1.1"
__author__ = "Elloit Aldersion"
__create_date__ = "2017-10-17"
"""
IP定位，GPS坐标的获取
以及DNS的反查
"""
# coding = UTF-8
# !/usr/bin/env python3

import requests
from lxml import etree
from fake_useragent import UserAgent
from math import ceil


class DomainInfo(object):

    def __init__(self, ip):
        self.ua = UserAgent()
        self.ip = ip

    def getDnsInfo(self, page=1):
        url = "https://dns.aizhan.com/" + self.ip + "/" + str(page) + "/"
        head = {
            "User-Agent": self.ua.random
        }
        re = requests.get(url=url, headers=head)
        responce = etree.HTML(re.text)
        domain_dict = {}
        lis = responce.xpath('//div[@class="dns-infos"]/ul/li')
        ip = lis[0].xpath("./strong/text()")
        addrs = lis[1].xpath("./strong/text()")
        numbrs = lis[2].xpath("./span/text()")
        try:
            domins = []
            trs = responce.xpath(
                '//div[@class="dns-content"]/table/tbody/tr')
            for tr in trs:
                tds = tr.xpath("./td")
                domin = tds[1].xpath("./a/@href")[0]
                title = tds[2].xpath("./span/text()")[0]
                domins.append([domin, title])
            domain_dict["addrs"] = addrs
            domain_dict["domins"] = domins
            pages = ceil(int(numbrs[0]) / 20)
            if page < pages:
                return self.getDnsInfo(page=page+1)

        except Exception as e:
            print(e)
            domain_dict["addrs"] = addrs
            domain_dict["domins"] = []
        return domain_dict

    def getIpInfo(self):
        url = "https://ipaddress.ip-adress.com/" + self.ip
        head = {
            "User-Agent": self.ua.random
        }
        re = requests.get(url=url, headers=head)
        responce = etree.HTML(re.text)
        trs = responce.xpath('//table[@class="vtable"]/tbody/tr')
        ipinfo_dict = {}
        for tr in trs:
            try:
                th = tr.xpath("./th/text()")[0]
                td = tr.xpath("./td/text()")[0]
                th = th.replace(" ", "")
                ipinfo_dict[th] = td
            except Exception as e:
                pass
        return ipinfo_dict
if __name__ == '__main__':

    print(DomainInfo("106.15.200.166").getDnsInfo())
    print(DomainInfo("106.15.200.166").getIpInfo())