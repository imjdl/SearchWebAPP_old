from subprocess import Popen , PIPE
from mysite.tools.Class_scan_host import scan_host
from mysite.tools.Class_get_data import getdata
from multiprocessing import Process
# cmd = ['sudo','-S','nmap','210.43.32.30','-O','-sS']
# cmd = ['sudo','-S','python3','Class_port_scan.py','10.100.47.246']
# passwd = '123qwe'
# p = Popen(cmd,stdin=PIPE,stderr=PIPE,universal_newlines=True,stdout=PIPE)
# output = p.communicate(passwd+'\n')
# data = list(output)
# data.pop()
# print(len(data))
# print("*"*10)
# datas = data[0].split("\n")
# for a in datas:
#     print(a,end="\n\n\n\n")
def run():
    get = getdata(0, "test2.csv")
    get.start()
    test = scan_host("203.66.65.94/24", "3389")
    test.scan()
    import time
    time.sleep(30)
    print(test.send.isAlive())
    # while not test.send.isAlive():
    get.stop()

p = Process(target=run)

p.start()