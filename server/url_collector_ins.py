import os
import time
from selenium.webdriver.common.keys import Keys
import config as cfg
import kkconn

current_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
def login(chromeDriver, conf):

    account_id = conf["ins"]["account"]["id"]
    account_pass = conf["ins"]["account"]["pass"]

    chromeDriver.get("https://www.instagram.com/")
    time.sleep(3)

    elem = chromeDriver.find_element_by_name("username")
    elem.send_keys(account_id)

    elem = chromeDriver.find_element_by_name("password")
    elem.send_keys(account_pass)
    elem.send_keys(Keys.RETURN)

    time.sleep(3)

def collect_urls(work):
    current_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
    conf = cfg.get_config(path=current_path)
    chromeDriver = cfg.get_chrome_driver(config_path=current_path)
    login(chromeDriver, conf)

    current_url_count = 0
    limit_url_count = conf["ins"]["limit_url_count"]
    keyword = work["keyword"]
    url = conf["ins"]["seed"]["collect"] + keyword.replace(' ', '')
    chromeDriver.get(url)
    time.sleep(3)

    while True:
        a_list = chromeDriver.find_elements_by_tag_name('a')
        url_list = []
        for a in a_list:
            try:
                url = a.get_attribute("href")
                if not str(url).find("https://www.instagram.com/p/"):
                    url_list.append(url)
            except:
                continue

        if len(url_list) == 0:
            continue

        kkconn.kafka_producer(url_list, work)
        current_url_count += len(url_list)
        print("Inserted {} URLS: {}, Current: {}".format(work["channel"], len(url_list), current_url_count))
        if current_url_count > limit_url_count:
            break

        chromeDriver.execute_script("window.scrollTo(0, window.scrollY - 50);")
        time.sleep(0.5)
        chromeDriver.execute_script("window.scrollTo(0, window.scrollY + 800);")

        time.sleep(3)


#
# if __name__ == "__main__":
#
#     work_list = [
#         {
#             "channel": "ins",
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
#         if work["channel"] == "ins":
#             collect_urls(work)
#
