import time
from bs4 import BeautifulSoup
import config as cfg
import datetime as dt
import os

current_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
def collect_urls(work):
    conf = cfg.get_config(path=current_path)
    chromeDriver = cfg.get_chrome_driver(config_path=current_path)

    work_group_no = work["work_group_no"]
    keyword = work["keyword"]
    start_date = work["start_date"]
    end_date = work["end_date"]

    csv_save_dir = conf["storage"]["csv_save_dir"]
    html_save_dir = conf["storage"]["html_save_dir"]
    filepath = cfg.get_save_dir(html_save_dir, work_group_no, "twt")

    keyword = keyword.replace('_', ' ')

    start_date = start_date.replace('-', '')
    start_date = dt.date(year=int(start_date[0:4]), month=int(start_date[4:6]), day=int(start_date[6:8]))

    end_date = end_date.replace('-', '')
    end_date = dt.date(year=int(end_date[0:4]), month=int(end_date[4:6]), day=int(end_date[6:8]))

    until_date = start_date + dt.timedelta(days=1)

    # while not end_date == start_date:
    url = 'https://twitter.com/search?q=' + keyword + '%20since%3A' + str(start_date) + '%20until%3A' + str(until_date)
    chromeDriver.get(url)
    lastHeight = chromeDriver.execute_script("return document.body.scrollHeight")

    file_no = 1
    while True:

        time.sleep(10 if file_no == 1 else 5)
        file_no += 1

        chromeDriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        newHeight = chromeDriver.execute_script("return document.body.scrollHeight")
        soup = BeautifulSoup(chromeDriver.page_source, "html.parser")

        cfg.make_dir(html_save_dir, work_group_no, ["twt"])
        cfg.make_dir(csv_save_dir, work_group_no, ["twt"])

        index = len(os.listdir(filepath))
        filename = cfg.get_save_filename("twt", work_group_no, keyword, str(start_date), index + 1, "html")
        save_file_path = filepath + filename

        with open(save_file_path, "w", encoding="utf-8") as f:
            f.write(str(chromeDriver.page_source))

        time.sleep(3)
        print('Written {}...'.format(save_file_path))

        if newHeight == lastHeight:
            start_date = until_date
            until_date += dt.timedelta(days=1)
            break

        lastHeight = newHeight

    chromeDriver.close()

# if __name__ == "__main__":
#
#     work_list = [
#         {
#             "channel": "twt",
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
