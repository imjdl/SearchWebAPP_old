# test.py
# coding = UTF-8
# !/usr/bin/env python3

import ctypes
import os
import socket
import fcntl
import struct

_file = "sendpack.so"

_path = os.path.join(*(os.path.split(__file__)[:-1] + (_file,)))

_mod = ctypes.cdll.LoadLibrary(_path)

sendData = _mod.senddata

sendData.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_char_p,
                     ctypes.c_char_p, ctypes.c_char_p)

sendData.restype = ctypes.c_int


def sendpack(syn, rst, src_ip, dst_ip, port):

    sendData(syn, rst, src_ip, dst_ip, port)


def get_ip_address(ifname):

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    return socket.inet_ntoa(fcntl.ioctl(

        s.fileno(),

        0x8915,  # SIOCGIFADDR

        struct.pack('256s', ifname[:15])

    )[20:24])


if __name__ == "__main__":
    src_ip = get_ip_address(b"wlan0")
    # dst_ip_file = os.path.join(*(os.path.split(__file__)[:-1] + ("ip_80.csv",)))
    # with open(dst_ip_file) as f:
    #     dst_ips = f.readlines()
    #     for dst_ip in dst_ips:
    #         sendpack(1, 0, src_ip.encode("UTF-8"), dst_ip.encode("UTF-8"), b"80")

    dst_ip = "10.100.59.110".encode("utf-8")
    for i in range(65535):
        port = str(i).encode("utf-8")
        sendpack(1, 0, src_ip.encode("UTF-8"), dst_ip, port)