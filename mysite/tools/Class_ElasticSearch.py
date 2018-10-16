__version__ = "SearchAPP_v1.1"
__author__ = "Elloit Aldersion"
__create_date__ = "2017-10-16"
"""
处理ElasticSearch 的数据搜索插入等操作
搜索部分介绍:
    搜索key:
    ip指定ip、app指定web容器、os指定操作系统、hostname指定域名、cidr指定cidr
    title指定的页面title
    联合使用 除ip之外
    单条件搜索：
        ip:127.0.0.1 或 app:apache 或 os:linux 或 hostname:google.com
        或 title:phpinfo 或CIDR:192.168.1.1/24 支持C 类地址等单个条件
    多条件搜索:
        如：app:apache;ver:2.4.0;
        或 os:linux;server:apache;
    版本更新：
    SearchAppV2---->>>>> SearchAppV3
    11月6日：增加了更详细的分组，新增title,prower,server 是搜索速度提升
"""

# coding = utf-8

# !/usr/bin/env python3

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import os,re,json


class ElasticSearch(object):

    _host = "127.0.0.1"
    _post = "9200"
    _es = None
    _index = "searchappv4"  # searchappv3 3号库兼容2号库
    _doc_type = "domains"

    def __init__(self):
        self._connect()
        self.choice = {
            "ip": self.search_ip,
            "os": self.search_os,
            "hostname": self.search_host,
            "app": self.search_app,
            "cidr": self.search_cidr,
            "title": self.search_title
        }

    def _connect(self):
        self._es = Elasticsearch(
            hosts=[{"host": self._host, "port": self._post}])

    def search(self, data=None, page=1):
        data_val = data
        if len(data) == 0:
            return self.search_read("", page)
        if len(data) == 1:
            try:
                key, value = data_val[0].split(':')
                try:
                    return self.choice[key](value, page)
                except KeyError as e:
                    return {"key error"}
            except ValueError as e:
                return self.search_read(data[0], page)
        elif len(data) > 5:
            return {"key error"}
        else:
            keys = []
            values = []
            for i in range(len(data_val)):
                try:
                    key, value = data_val[i].split(':')
                except BaseException:
                    return {"key error"}
                keys.append(key)
                values.append(value)
            # 所有key转小写
            for i in range(len(keys)):
                keys[i] = keys[i].lower()
            if "ip" in keys:
                return {"key error"}
            if "cidr" in keys:
                return {"key error"}
            if "hostname" in keys:
                return {"key error"}
            # 去除重复的key key不能重复
            keys_bak = set(keys)
            if len(keys) != len(keys_bak):
                return {"key error"}
            del keys_bak

            # 处理不存在的KEY
            for key in keys:
                if key not in ("os", "title", "app", "cidr", "hostname"):
                    return {"key error"}
            item = []
            for i in range(len(keys)):
                item.append({"match": {"server": values[i]}})
                item.append({"match": {"prower": values[i]}})
                item.append({"match": {"read": values[i]}})
            mybool = {
                "should": item
            }
            return self.search_union(mybool, page)

    def search_union(self, mybool=None, page=1):
        _querry = {
            "query": {
                "bool": mybool
            },
            "from": (page - 1) * 10,
            "size": 10
        }
        return self._es.search(
            index=self._index,
            doc_type=self._doc_type,
            body=_querry)

    def search_read(self, data=None, page=1):
        if data == "":
            _querry = {
                "query": {
                    "match_all": {}
                },
                "from": (page - 1) * 10,
                "size": 10
            }
        else:
            _querry = {
                "query": {
                    "match": {
                        "read": data
                    }
                },
                "from": (page - 1) * 10,
                "size": 10
            }
        return self._es.search(
            index=self._index,
            doc_type=self._doc_type,
            body=_querry)

    def search_os(self, data=None, page=1):
        _querry = {
            "query": {
                "bool": {
                    "should": [
                        {"term": {"server": data}},
                        {"term": {"prower": data}},
                        {"term": {"read": data}}
                    ]
                }
            },
            "from": (page - 1) * 10,
            "size": 10
        }
        return self._es.search(
            index=self._index,
            doc_type=self._doc_type,
            body=_querry)

    def search_title(self, data=None, page=1):
        _querry = {
            "query": {
                "match": {
                    "title": data
                }
            },
            "from": (page - 1) * 10,
            "size": 10
        }
        return self._es.search(
            index=self._index,
            doc_type=self._doc_type,
            body=_querry)

    def search_app(self, data=None, page=1):
        _querry = {
            "query": {
                "bool": {
                    "should": [
                        {"term": {"server": data}},
                        {"term": {"prower": data}},
                        {"term": {"read": data}}
                    ]
                }
            },
            "from": (page - 1) * 10,
            "size": 10
        }
        return self._es.search(
            index=self._index,
            doc_type=self._doc_type,
            body=_querry)

    def search_host(self, data=None, page=1):
        """
        data 的错误判断
        """
        res = os.popen("host -t a " + data, "r", -1)
        res = res.readlines()
        ips = []
        for item in res:
            ip = item.split(" ")[-1].replace("\n", "")
            ips.append(ip)
        return self.search_ip(ips, page)

    def search_cidr(self, data=None, page=1):
        """
        没有对数据进行判断
        """
        # 当不合法时此处报错
        ip, type_ip = data.split("/")
        ips = ip.split(".")
        if type_ip == "24":
            ips.pop()
            new_ip = ".".join(ips)
            new_ips = []
            for i in range(1, 256):
                new_ips.append(new_ip + "." + str(i))
            return self.search_ip(new_ips, page)
        else:
            # 错误处理
            pass

    def search_ip(self, data=None, page=1):
        """
        可以查询单个或多个ip
        """
        if not isinstance(data, list):
            data = [data]
        _querry = {
            "query": {
                "terms": {
                    "ip": data
                }
            },
            "from": (page - 1) * 10,
            "size": 10
        }
        del data
        return self._es.search(
            index=self._index,
            doc_type=self._doc_type,
            body=_querry)

    def getData_number(self):
        _querry = {
            "query": {
                "match_all": {}
            },
            "from": 0,
            "size": 0
        }
        return self._es.search(
            index=self._index,
            doc_type=self._doc_type,
            body=_querry)

    def getRead(self, ip):
        _querry = {
            "query": {
                "match": {
                    "ip": ip
                }
            }
        }
        return self._es.search(
            index=self._index,
            doc_type=self._doc_type,
            body=_querry
        )["hits"]["hits"][0]["_source"]["read"]

    def get_webapps_num(self):
        """
        获取web应用
        """
        appslist = [{
            "name": "WordPress",
            "value": 0
        },
            {
                "name": "phpMyAdmin",
                "value": 0
        },
            {
                "name": "Joomla",
                "value": 0
        },
            {
                "name": "DedeCMS",
                "value": 0
        },
            {
                "name": "LiteSpeed",
                "value": 0
        },
            {
                "name": "Drupal",
                "value": 0
        },
            {
                "name": "FCKeditor",
                "value": 0
        },
            {
                "name": "CKEditor",
                "value": 0
        },
            {
                "name": "Discuz!",
                "value": 0
        },
            {
                "name": "RoundCube",
                "value": 0
        },
            {
                "name": "Magento",
                "value": 0
        },
            {
                "name": "Shopify",
                "value": 0
        },
            {
                "name": "Z-Blog",
                "value": 0
        },
            {
                "name": "phpBB",
                "value": 0
        },
            {
                "name": "phpcms",
                "value": 0
        },
            {
                "name": "ZenCart",
                "value": 0
        },
            {
                "name": "Invision Power Board",
                "value": 0
        },
            {
                "name": "ECShop",
                "value": 0
        },
            {
                "name": "osCommerce",
                "value": 0
        }
        ]
        nums = 0
        for i in appslist:
            i["value"] = self.get_webapp_num(i["name"])
            nums = nums + int(i["value"])
        appslist = sorted(appslist, key=lambda k: k["value"])
        appslist.append({"nums": nums})
        return appslist

    def get_zujian_num(self):
        product = [
            {
                "name": "Apache httpd",
                "value": 0
            },
            {
                "name": "OpenSSH",
                "value": 0
            },
            {
                "name": "Dropbear sshd",
                "value": 0
            },
            {
                "name": "Allegro RomPager",
                "value": 0
            },
            {
                "name": "AkamaiGHost",
                "value": 0
            },
            {
                "name": "gSOAP soap",
                "value": 0
            },
            {
                "name": "nginx",
                "value": 0
            },
            {
                "name": "Microsoft IIS httpd",
                "value": 0
            },
            {
                "name": "Portable SDK for UPnP devices",
                "value": 0
            },
            {
                "name": "MySQL",
                "value": 0
            },
            {
                "name": "Microsoft HTTPAPI httpd",
                "value": 0
            },
            {
                "name": "TR-069 remote access",
                "value": 0
            },
            {
                "name": "lighttpd",
                "value": 0
            },
            {
                "name": "Microsoft Windows RPC",
                "value": 0
            },
            {
                "name": "Exim smtpd",
                "value": 0
            },
            {
                "name": "Microsoft Terminal Service",
                "value": 0
            },
            {
                "name": "Dovecot imapd",
                "value": 0
            },
            {
                "name": "mini_httpd",
                "value": 0
            },
            {
                "name": "Dovecot pop3d",
                "value": 0
            }
        ]
        nums = 0
        for i in product:
            i["value"] = int(self.get_webapp_num(i["name"]))
            nums = nums + i["value"]
        product = sorted(product, key=lambda k: k["value"])
        product.append({"nums": nums})
        return product

    def delete_data(self, ip):
        """
        这里说明一下:删除操作只删除 搜索引擎的 IP记录 ,Mysql里的端口数据不应删除
        应为只要没有 IP记录 ,Mysql 里对应数据就为不可见。
        """
        try:
            self._es.delete(index=self._index, doc_type=self._doc_type, id=ip)
            return True
        except Exception as e:
            return False

    def get_webapp_num(self, data):
        _querry = {
            "query": {
                "bool": {
                    "should": [
                        {"match": {"server": data}},
                        {"match": {"prower": data}},
                        {"match": {"read": data}}
                    ]
                }
            },
            "size": 1
        }
        res = self._es.search(
            index=self._index,
            doc_type=self._doc_type,
            body=_querry)

        return res["hits"]["total"]

    def post(self,datas, index = "searchappv4"):
        """
        批量倒入
        """
        bulk(self._es, datas, index=index)

    def insert_data(self,datas):
        data = datas
        action = []
        for i in range(len(data)):
            data[i] = json.loads(data[i])
            try:
                read = data[i]["data"]["read"]
                server = re.findall(r"Server:.*\r\n", read)
                if server == []:
                    server = "Unknown"
                else:
                    server = server[0].replace("Server: ", "").strip()
                prower = re.findall(r"X-Powered-By:.*\r\n", read)
                if prower == []:
                    prower = "Unknown"
                else:
                    prower = prower[0].replace(
                        "X-Powered-By:", "").strip()
                title = re.findall(r"<title>(.*?)</title>", read)
                if title == []:
                    title = "Unknown"
                else:
                    title = title[0]
                datas = {
                    "_index": "searchappv4",
                    "_type": "domains",
                    "_id": data[i]["ip"],
                    "ip": data[i]["ip"],
                    "server": server,
                    "prower": prower,
                    "title": title,
                    "timestamp": data[i]["timestamp"],
                    "read": read
                }
            except:
                datas = {
                    "_index": "searchappv4",
                    "_type": "domains",
                    "_id": data[i]["ip"],
                    "ip": data[i]["ip"],
                    "server": "Unknown",
                    "prower": "Unknown",
                    "title": "Unknown",
                    "timestamp": data[i]["timestamp"],
                    "read": None
                }
            action.append(datas)
        self.post(action)

if __name__ == '__main__':
    res = ElasticSearch()
    # print(res.delete_data("106.15.200.166"))

    # res = os.popen("host -t a baidu.com","r",-1)
    # res = res.readlines()
    # ips = []
    # for item in res:
    #     ip = item.split(" ")[-1].replace("\n","")
    #     ips.append(ip)
    # print(ips)

    with open("/root/project/SearchApp/data/hist.json", "r") as f:
        datas = f.readlines()
    res.insert_data(datas)