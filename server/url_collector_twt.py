import time
from bs4 import BeautifulSoup
import config as cfg
import datetime as dt
import os
import text_extractor as te
import datetime as pydatetime

current_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
def collect_urls(work):
    conf = cfg.get_config(path=current_path)
    chromeDriver = cfg.get_chrome_driver(config_path=current_path)

    work_group_no = work["work_group_no"]
    keyword = work["keyword"]
    start_date = work["start_date"]
    end_date = work["end_date"]
    csv_save_dir = work["csv_save_dir"]
    html_save_dir = work["html_save_dir"]
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

        cfg.make_dir(html_save_dir, work_group_no, ["twt"])
        cfg.make_dir(csv_save_dir, work_group_no, ["twt"])

        index = len(os.listdir(filepath))
        date = str(start_date).replace('-', '')
        filename = cfg.get_save_filename("twt", work_group_no, keyword, date, index + 1, "html")
        save_file_path = filepath + filename

        work["source"] = str(chromeDriver.page_source)
        work["index"] = file_no

        html_save_path = work["html_save_dir"]
        curreunt_timestamp = str(pydatetime.datetime.now()).split('.')[0]

        html_log_file_path = html_save_path + '/logs.txt'
        if not os.path.isfile(html_log_file_path):
            with open(html_log_file_path, "w", encoding="utf-8") as f:
                f.write("[twt][{}] {}\n".format(curreunt_timestamp, work["source"][0:50]))
        else:
            with open(html_log_file_path, "a", encoding="utf-8") as f:
                f.write("[twt][{}] {}\n".format(curreunt_timestamp, work["source"][0:50]))

        origin_save_path = work["csv_save_dir"] + '/origin'
        if not os.path.isdir(origin_save_path):
            os.makedirs(origin_save_path, exist_ok=True)

        filename = '{}_{}.csv'.format("twt", date)
        origin_save_path = origin_save_path + '/' + filename
        work["filename"] = filename
        extracted_text = te.extract(work)

        if not os.path.isfile(origin_save_path):
            with open(origin_save_path, 'w', encoding="utf-8") as f:
                f.write("text,keyword,date,channel\n")
        else:
            with open(origin_save_path, 'a', encoding="utf-8") as f:
                f.write("{},{},{},{}\n".format(extracted_text, keyword, date, "twt"))

            print("[{}] Added Text: {}".format(file_no, extracted_text[0:50]))

        # with open(save_file_path, "w", encoding="utf-8") as f:
        #     f.write(str(chromeDriver.page_source))

        time.sleep(3)
        # print('Written {}...'.format(save_file_path))

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
