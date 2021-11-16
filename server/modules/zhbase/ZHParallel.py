import time
from multiprocessing import Process, Pool, Value
import multiprocessing as mp


class ZHParallel:

    def __init__(self):
        self.p_list = []

    def add(self, func, params):
        self.p_list.append(Process(target=func, args=params))

    def pool(self, func, items):
        pool = Pool(mp.cpu_count() * 2)
        result = pool.map(func, items)
        return result

    def start(self):
        for p in self.p_list:
            p.collect_probed_urls()


class ZHTest:
    def test(self, intz):
        for i in range(0, 100):
            print("{}-{}".format(intz, i))
            time.sleep(0.5)


# if __name__ == "__main__":
#     zt = ZHTest()
#     t = ZHParallel()
#     t.add(zt.test, (1,))
#     t.add(zt.test, (2,))
#     t.start()

