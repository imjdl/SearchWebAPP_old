# !/usr/bin/env python3

#coding = UTF-8

import requests
import os,sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
print(os.path.dirname(os.path.abspath(__file__)))
print(os.path.abspath(__file__))
with open("test2.csv") as ips:
    ips = ips.readlines()

# for i in ips:
#     i = i.strip()
#     print(i.strip())
    # try:
    #     r = requests.get(url="http://"+i+"/")
    #     print(r.headers)
    # except Exception as e:
    #     pass
#

hd = {"user-agent":"EtaoSpider"}
proxies = { "http": "http://127.0.0.1:8080","https": "http://127.0.0.1:8080"  }
# r = requests.request(method="get",url="https://www.jd.com",headers=hd,timeout=30,proxies=proxies)
# r.encoding = "utf-8"
# print(r.headers)
# print(r.text)
r = requests.get("http://ip.chinaz.com/", proxies=proxies, headers=hd)
print(r.headers)
print(r.text)



