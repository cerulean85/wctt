import math
import re
import time
from abc import ABC

from bs4 import BeautifulSoup
import config as cfg
import modules.collect.dir as dir

# import dbconn
from modules.collect.scrap.SCScrapper import SCScrapper


class SCBlogNaver(SCScrapper, ABC):

    def __init__(self, work):
        super().__init__(work)
        self.chromeDriver = cfg.get_chrome_driver(config_path=dir.config_path)

    def collect_probed_urls(self):
        # self._probe()
        self._collect_urls()
        self.chromeDriver.quit()

    def _probe(self):
        url = cfg.get_probe_url(self.channel, self.keyword, self.start_date, self.end_date, config_path=dir.config_path)
        self.chromeDriver.get(url)
        time.sleep(5)
        item = self.chromeDriver.find_element_by_xpath('//*[@id="content"]/section/div[1]/div[2]/span/span/em')

        try:
            _totalCountStr = item.text.replace(' ', '')
            _totalCountStr = _totalCountStr.replace('건', '')
            _totalCountStr = _totalCountStr.replace(',', '')
            self.pred_total_article_count = int(_totalCountStr)
            self.pred_total_page_count = int(math.ceil(self.pred_total_article_count / 7))

        except Exception as err:
            print(err)

    def _get_url(self, target_page_no):
        url_set = set([])
        if int(target_page_no) > 0:
            url = cfg.get_collect_url(self.channel, target_page_no, self.keyword, self.start_date, self.end_date, config_path=dir.config_path)
            self.chromeDriver.get(url)

            conf = cfg.get_config(path=dir.config_path)
            time.sleep(conf[self.channel]["delay_time"]) # Crome Drive가 소스를 받는데 시간이 필요함
            soup = BeautifulSoup(self.chromeDriver.page_source, "html.parser")
            try:
                items = soup.find_all('a')

                patterns = "http[s]{0,1}://blog.naver.com/[a-zA-Z0-9_]+/[a-zA-Z0-9_]+"
                for item in items:
                    m = re.match(patterns, item["href"])
                    if m is not None:
                        url_set.add(item["href"])

            except Exception as e:
                print(e)

        return url_set

    def _collect_urls(self):

        target_page_no = 1
        while True:
        # for target_page_no in range(1, self.pred_total_page_count + 1):
            try:
                url_set = self._get_url(target_page_no)

                url_o_list = []
                for url in list(url_set):
                    url_o_list.append(url)

                if len(url_o_list) > 0:
                    # DBHandler().insert_urls(url_o_list, self.work)
                    # Kafka
                    print("Inserted {} URLS: {}".format(self.channel, len(url_o_list)))

                target_page_no += 1

            except Exception as e:
                print(e)

                    # if target_page_no == 572:
                    #     break




# if __name__ == "__main__":
#     scb = SCBlogNaver()
#     scb.start("코로나_백신", "2021-02-26", "2021-06-30")