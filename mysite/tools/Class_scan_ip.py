# Class_scan_ip.py

# coding = UTF-8

# !/usr/bin/env python3

__author__ = "elloit"

__doc__ = """

加载动态链接库
扫描 一个c段 ip

"""

import ctypes
import os
import socket
import fcntl
import struct
from threading import Thread
from mysite.tools.Class_get_data import getdata


class scan_ip(Thread):

    _file = "myrawsocket.so"
    _path = os.path.join(*(os.path.split(__file__)[:-1] + ("c_dir/", _file,)))
    _mod = ctypes.cdll.LoadLibrary(_path)
    _flage = True

    def __init__(
            self,
            syn=1,
            rst=0,
            ifname="wlan0",
            dst_ip="127.0.0.1",
            port="80",
            scan_port=False):
        Thread.__init__(self)
        self.syn = syn
        self.rst = rst
        self.src_ip = self._get_ip_address(ifname.encode("UTF-8"))
        self.dst_ip = dst_ip
        self.port = port
        self.scan_port = scan_port

    def _sendpack(self, dst_ip, port):

        sendData = self._mod.senddata

        sendData.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_char_p,
                             ctypes.c_char_p, ctypes.c_char_p)

        sendData.restype = ctypes.c_int

        sendData(
            self.syn,
            self.rst,
            self.src_ip.encode("UTF-8"),
            dst_ip.encode("UTF-8"),
            port.encode("UTF-8"))

    def _get_ip_address(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])

    def _scan_host(self):
        for i in range(1,256):
            ip = self.dst_ip + "." + str(i)
            print(ip)
            self._sendpack(ip, self.port)

    def _scan_port(self):
        print("scan_port begin")
        for i in range(65535):
            if self._flage:
                self._sendpack(self.dst_ip, str(i))
            else:
                break
        print("scan_port end")

    def run(self):
        print("sendrun")
        if self.scan_port:
            self._scan_port()
        else:
            self._scan_host()

    def stop(self):
        self._flage = False


if __name__ == '__main__':
    for i in range(1,256):
        send = scan_ip(1, 0, "wlan0", "106.15." + str(i), "80")
        send.start()
