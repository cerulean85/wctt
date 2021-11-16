import abc
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class SCScrapper:

    def __init__(self, work):
        self.url_list = []
        self.pred_total_article_count = 0
        self.pred_total_page_count = 0
        self.keyword = work["keyword"]
        self.start_date = work["start_dt"]
        self.end_date = work["end_dt"]
        self.channel = work["channel"]
        self.work = work

    @abc.abstractmethod
    def collect_probed_urls(self):
        pass

    # @abc.abstractmethod
    # def collect_docs_from_urls(self, work):
    #     pass

    @abc.abstractmethod
    def _probe(self):
        pass

    @abc.abstractmethod
    def _collect_urls(self):
        pass

    @abc.abstractmethod
    def _get_url(self, target_page_no):
        pass

    def write_file(self, file_info):
        filepath = file_info["filepath"]
        filename = file_info["filename"]
        source = str(file_info["source"])
        with open(filepath + '/' + filename, "w", encoding="utf-8") as f:
            f.write(source)
        print('Written {}...'.format(filename))

    def print_url(self, url):
        print(url)
# if __name__ == "__main__":
#     SCScrapperChild()
#     scs = SCScrapper()
#     scs.login()
#     scs.get_web_doc(scs.get_url_list())
#
