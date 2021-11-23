import os
import time
from bs4 import BeautifulSoup
import config as cfg
import kkconn

current_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
conf = cfg.get_config(path=current_path)
def get_url(work, target_page_no, chromeDriver, conf):
    url_set = set([])

    if int(target_page_no) > 0:
        channel = work["channel"]
        keyword = work["keyword"]
        start_date = work["start_date"]
        end_date = work["end_date"]
        url = cfg.get_collect_url(channel, target_page_no, keyword, start_date, end_date, config_path=current_path)
        chromeDriver.get(url)

        time.sleep(conf[channel]["delay_time"])  # Crome Drive가 소스를 받는데 시간이 필요함
        soup = BeautifulSoup(chromeDriver.page_source, "html.parser")
        try:
            items = soup.find_all('a')
            for item in items:
                url_set.add(item["href"])

        except Exception as e:
            print(e)

    return url_set


def collect_urls(work, q):
    chromeDriver = cfg.get_chrome_driver(config_path=current_path)

    current_url_count = 0
    channel = work["channel"]
    limit_url_count = conf[channel]["limit_url_count"]
    target_page_no = 1
    while True:
        try:
            url_count = 0
            url_set = get_url(work, target_page_no, chromeDriver, conf)
            for url in list(url_set):
                q.put(url)
                url_count += 1

            if url_count > 0:
                current_url_count += url_count
                print("Inserted {} URLS: {}, Current: {}".format(work["channel"], url_count, current_url_count))

            if current_url_count > limit_url_count:
                break

            target_page_no += 1

        except Exception as e:
            print(e)

    chromeDriver.close()
# if __name__ == "__main__":
#
#     work_list = [
#         {
#             "channel": "dna",
#             "keyword": "코로나 백신",
#             "start_date": "2021-09-01",
#             "end_date": "2021-09-30",
#             "work_type": "collect_url",
#             "work_group_no": 2,
#         }
#
#     ]
#
#     for work in work_list:
#         date_list = date_range("2021-09-01", "2021-09-30")
#         for date in date_list:
#             work["start_date"] = date
#             work["end_date"] = date
#             collect_urls(work)
