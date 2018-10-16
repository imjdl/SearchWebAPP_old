# Class_get_banner.py
__author__ = "Elliot"
__date__ = "2017-10-19"
__doc__ = """
获取banner 信息
形参：IP地址(str)、代理服务器(dict)如果你需要的话 、端口(int)默认80、timeout(int)默认10s
返回值: dict such as:
{
    "IP":"127.0.0.1",
    "timestamp": "2017-10-19T23:50:20+08:00",
    "data":{
        "read":"这里有http返回的头部信息和页面",
        "write":"GET / HTTP/1.1\nHost: 127.0.0.1\n\n"
    }
}
代理服务器说明:字典格式为:{"http":"user:pass@127.0.0.1:8080"}
或{"https":"https://127.0.0.1:8888"}

"""
import requests


class Get_Banner:
    """
    默认的请求User-Agent
    建议不要修改，遵守robots协议
    """
    _head = {
        "user-agent": "SearchApp",
        "host":"www.baidu.com"
    }

    def __init__(self, ip, pxs=None, port=80, timeout=10):
        self._ip = ip
        self._port = port
        self._pxs = pxs
        self._timeout = timeout
        self._url = "http://" + ip + ":" + str(port)

    def getbanner(self):
        req = requests.request(
            method="get",
            url=self._url,
            proxies=self._pxs,
            headers=self._head,
            timeout=self._timeout)
        req.encoding = "UTF-8"
        reslut = {}
        reslut["data"] = {}
        reslut["ip"] = self._ip
        reslut["timestamp"] = req.headers["Date"].strip()
        req.headers.pop("Date")
        # head = dict(req.headers)
        # head = str(head).strip("{")
        # head = head .strip("}")
        # head = head.replace("\'","")
        # head = head.replace("\"", "")
        head = ""
        for k,v in req.headers.items():
            head = head + k + ":" + v +"\r\n"

        text = req.text.replace("\"","")
        text = text.replace("\'","")
        # print(text)
        reslut["data"]["read"] = "HTTP/1.1 " + str(req.status_code) + "\r\n" + \
                                 head + text
        write = str(self._head)
        write = write.strip("}")
        write = write.strip("{")
        write = write.replace("\'","")
        reslut["data"]["write"] = write
        return reslut

    def set_http_head(self, head):
        """
        自定义 请求头
        """
        self._head = head


if __name__ == '__main__':
    import sys
    import os
    # import json
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    test = Get_Banner(ip="106.15.200.166", port=80, timeout=20)
    # f = open("123.json","a")
    res = str(test.getbanner())
    # re.sub(r"(,?)(\w+?)\s*?:", r"\1'\2':",res)
    res = res.replace("\'","\"")
    # res = res.replace("\\","")
    # print(res)
    # f.writelines(res)
    # f.close()

    # json.loads(res)
    print(res)
    from mysite.tools.Class_ElasticSearch import ElasticSearch
    e = ElasticSearch()
    e.insert_data([res])