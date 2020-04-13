"""
获取系统健康信息utils

| 环境 | 指标  |
| ---  | ---  | 
| systeam | cpu  |
| systeam | 内存 |
| systeam | i/o  |
| systeam | 磁盘 |
|  PID |  cpu  |
|  PID |  内存 |
|  PID |  i/o |
|  PID |  磁盘 |
|  PID |  所在目录 |
"""

import os
import subprocess


def systeam_health():
    """
    dstat命令
    -c enable cpu stats (system, user, idle, wait, hardware interrupt, software interrupt)
    -l enable load average stats (1 min, 5 mins, 15mins)
    -m enable memory stats (used, buffers, cache, free)
    -n enable network stats (receive, send)
    -r enable I/O request stats (read, write requests)
    """
    #  ----total-cpu-usage---- ---load-avg--- ------memory-usage----- -net/total- --io/total-
    # usr sys idl wai hiq siq| 1m   5m  15m | used  buff  cach  free| recv  send| read  writ
    #   3   2  95   0   0   0|0.19 0.12 0.09|1014M  138M  724M  124M|   0     0 |0.07  0.94 

    cmd = """dstat -clmnr -N total  5 1 |tail -n1"""
    r = subprocess.getoutput(cmd).split(" ")
    rr = [m for i in r if i != "" or "|" in i for m in i.split("|") if m != ""]
    #return rr
    
def ts():
    a = "  0   0 100   0   0   0|0.05 0.03 0.01| 811M  160M  763M  237M| 224B   12B|   0     0"
    b = a.split(" ")
    d = {}
    rr = [m for i in b if i != "" or "|" in i for m in i.split("|") if m != ""]
    #for i in b:
    #    if i != "" or "|" in i:
    #        c = i.split("|")
    #        for m in c:
    #            if m != "":
    #                rr.append(m)
                #for m in c:
                #    if m != "":
                #        rr.append(m)
                #        print(m)
            #rr.append(i)



def pid_list():
    """
    获取所有的PID
    :return :pid_list
    """
    cmd = """ps -aux |awk '{print $2}'"""
    #res = os.popen(cmd).readlines()
    r = subprocess.getoutput(cmd)
    res = r.split("\n")[1:]
    return res

def pid_cwd(pid):
    """
    获取pid所在目录
    :return :pid_pwd
    """
    cmd = """pwdx %s""" % pid
    res = subprocess.getoutput(cmd)
    return res

def pid_headlth(pid):
    """
    获取pid cpu 内存 虚拟内存
    :return :pid_headlth_dict
    """
    cmd = """top -p """ % pid
    res = subprocess.getoutput(cmd)
    return res

if __name__ == '__main__':
    #pids = pid_list()
    #for pid in pids: print(pid_cwd(pid))
    #a = systeam_health()
    #print(a)
    ts()


