# Class_ipinfo

__author__ = "elloit"

__date__ = "2017-10-12"

__doc__ = """
获取 IP 的详细信息
国家、城市、坐标
"""
import os
import geoip2.database

_file = "data"
_path = os.path.join(
    *(os.path.split(__file__)[:-1] + ("data/ipinfo/", _file,)))


class ipinfo(object):

    def __init__(self, ip):
        self.ip = ip

    def get_ipinfo(self):
        ip_data = {}
        reader = geoip2.database.Reader(_path)
        responce = reader.city(ip_address=self.ip)
        ip_data["location"] = {}
        ip_data["location"]["latitude"] = responce.location.latitude
        ip_data["location"]["longitude"] = responce.location.longitude
        ip_data["time_zone"] = responce.location.time_zone
        ip_data["country"] = responce.registered_country.name
        ip_data["city"] = responce.city.name
        ip_data["continent"] = responce.continent.name
        return ip_data


if __name__ == '__main__':
    print(ipinfo("210.43.32.30").get_ipinfo())
