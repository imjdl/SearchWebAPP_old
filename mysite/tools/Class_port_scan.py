import nmap
from multiprocessing import Pool

class port_scan(object):

    def __init__(self, dst_ip):
        self.dst_ip = dst_ip

    def scan_port(self, portlist=None):
        data = {}
        data["ports"] = []
        scan = nmap.PortScanner()
        result = scan.scan(
            hosts=self.dst_ip,
            ports=portlist,
            arguments="-O -sS",sudo=False)
        try:
            data["hostname"] = result["scan"][self.dst_ip]["hostnames"][0]["name"]
            data["os"] = result["scan"][self.dst_ip]["osmatch"][0]["name"]
            for key, value in result["scan"][self.dst_ip]["tcp"].items():
                data["ports"].append({"port":key,"value": value})
        except:
            pass
        return data

    def getlist(self):
        ports = []
        with open("data/port_list.txt", "r") as p:
            port = p.readline()
            port = port.split(",")
        for i in range(0, len(port), 100):
            ports.append(",".join(port[i:100 + i]))
        return ports
    def run(self):
        pool = Pool(10)


if __name__ == '__main__':
    import sys
    ip = sys.argv[1]
    port = port_scan(dst_ip=ip)
    res = port.scan_port()
    print(res)