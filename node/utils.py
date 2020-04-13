import time
import queue

def spend_time(func):
    """
    计算函数运行时间
    :param func:
    :return: 函数运行时间
    """
    def newFunc(*args, **args2):
        t0 = time.time()
        start_time = "%s" % (time.strftime("%X", time.localtime()))
        back = func(*args, **args2)
        end_time = "%s" % (time.strftime("%X", time.localtime()))
        spend_time = "%.3fs" % (time.time() - t0)
        print("{func}函数运行时间{time}".format(time=spend_time, func=func))
        return back
    return newFunc

def set_url_queue(url_list):
    que = queue.Queue()
    for url in url_list: que.put(url) 
    return que

def ts():
    url_list = ["https://www.xicidaili.com/nn/%s" % i for i in range(100)]
    que = set_url_queue(url_list)
    return que

if __name__ == '__main__':
    url_list = ["https://www.xicidaili.com/nn/%s" % i for i in range(100)]
    que = set_url_queue(url_list)