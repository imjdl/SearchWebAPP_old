
import ctypes
import os
from threading import Thread


class getdata(Thread):

    _file = "myrawsocket.so"

    _path = os.path.join(*(os.path.split(__file__)[:-1] + ("c_dir/", _file,)))
    _mod = ctypes.cdll.LoadLibrary(_path)

    def __init__(os:linuxself, isip, filename):
        Thread.__init__(self)
        self.isip = isip
        self.filename = filename

    def _getbackdata(self):
        """
        isip
        0 ---->>> ip
        !0 ---->>> port
        """
        getData = self._mod.getdata
        getData(self.filename.encode("utf-8"), self.isip)

    def run(self):
        self._getbackdata()

    def stop(self):
        signal = self._mod.stop
        signal()


if __name__ == '__main__':
    get = getdata(0, "test2.csv")
    get.start()
    import time
    time.sleep(60)
    get.stop()