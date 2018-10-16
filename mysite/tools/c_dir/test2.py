# test2.py

# coding = UTF-8

# !/usr/bin/env python3

import ctypes
import os

_file = "getpack.so"

_path = os.path.join(*(os.path.split(__file__)[:-1] + (_file,)))

_mod = ctypes.cdll.LoadLibrary(_path)

getData = _mod.getdata

if __name__ == '__main__':
    # 0的话记录ip 非0记录端口
    filename = "file_ip.csv".encode("utf-8")
    getData(filename, 1)
