# Class_get_system.py

__doc__ = """
获取系统状态
"""

import psutil
import time
class Get_System(object):
    def get_cpu(self):
        count = psutil.cpu_count()
        cpu = []
        for i in range(count):
            cpu.append(psutil.cpu_percent(i))
        return cpu
    def get_ip(self):
        return psutil.net_if_addrs()["wlan0"][0].address
    def get_memory(self):
        memory = psutil.virtual_memory()
        return {"total":float("%.2f"%(memory.total/(1024**3))),"used":float("%.2f"%(memory.used/(1024**3))),"percent":memory.percent}

    def get_disk(self):
        disk = psutil.disk_partitions()
        datas = []
        for i in disk:
            name = i.mountpoint
            mountpoint = psutil.disk_usage(name)
            datas.append({"device":i.device,"name":name,"total": float("%.2f" % (mountpoint.total / (1024 ** 3))),
                    "used": float("%.2f" % (mountpoint.used / (1024 ** 3))),
                    "percent": mountpoint.percent})
        return datas
    def get_net_speed(self):
        befor_sned = psutil.net_io_counters().bytes_sent
        befor_recv = psutil.net_io_counters().bytes_recv
        time.sleep(1)
        after_send = psutil.net_io_counters().bytes_sent
        after_recv = psutil.net_io_counters().bytes_recv
        speed = {}
        speed["send_speed"] = self.bytes2human(after_send-befor_sned)
        speed["recv_speed"] = self.bytes2human(after_recv-befor_recv)
        return speed

    def bytes2human(slef,n):
        """
        >>> bytes2human(10000)
        '9.8 K'
        >>> bytes2human(100001221)
        '95.4 M'
        """
        symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
        prefix = {}
        for i, s in enumerate(symbols): # 枚举类型 0 k 1 M ...
            prefix[s] = 1 << (i + 1) * 10
        for s in reversed(symbols):
            if n >= prefix[s]:
                value = float(n) / prefix[s]
                return '%.2f %s' % (value, s)
        return '%.2f B' % (n) # 小于1K的数据
    def get_process(self):
        return [p.info for p in psutil.process_iter(attrs=['pid', 'name', 'username','create_time','cpu_percent']) ]

    def get_boot_time(self):
        return psutil.boot_time()

if __name__ == '__main__':
    print(Get_System().get_memory())
    print(Get_System().get_disk())
    print(Get_System().get_cpu())
    print(Get_System().get_boot_time())