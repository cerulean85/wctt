import time
from multiprocessing import Process
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

import parallel as prl
import config as cfg
import kkconn
import modules.collect.dir as dir
from datetime import datetime, timedelta
import datetime as dt
import os

conf = cfg.get_config(path=dir.config_path)
chromeDriver = cfg.get_chrome_driver(config_path=dir.config_path)


def date_range(start, end):
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end - start).days + 1)]
    return dates


def login(channel):
    if channel == "ins":
        domain = conf["ins"]["domain"]
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
        # elem = chromeDriver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div/div/button")
        # chromeDriver.execute_script("arguments[0].click();", elem)
        #
        # time.sleep(2)
        # elem = chromeDriver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]")
        # chromeDriver.execute_script("arguments[0].click();", elem)


def collect_urls(work):
    work_type = "collect_url"
    print(work_type)

    # for work in works:
    #     prl.stop_procs(work)

    # for work in works:
    channel = work["channel"]
    direct_page_download = conf[channel]["direct_page_download"]
    data_load_method = conf[channel]["data_load_method"]

    try:
        login(channel)
    except Exception as e:
        print("이미 로그인됨")


    if not direct_page_download:
        if data_load_method == "page_nav":
            collect_urls_by_page_nav(work)
            # prl.add_proc(work, Process(target=collect_urls_by_page_nav, args=(work,)))
        else:
            collect_urls_by_inf_scorll(work)
            # prl.add_proc(work, Process(target=collect_urls_by_inf_scorll, args=(work,)))
        # prl.start_procs(work_type)


def get_url(work, target_page_no):
    url_set = set([])

    if int(target_page_no) > 0:
        channel = work["channel"]
        keyword = work["keyword"]
        start_date = work["start_date"]
        end_date = work["end_date"]
        url = cfg.get_collect_url(channel, target_page_no, keyword, start_date, end_date, config_path=dir.config_path)
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


def collect_urls_by_page_nav(work):
    current_url_count = 0
    channel = work["channel"]
    limit_url_count = conf[channel]["limit_url_count"]
    target_page_no = 1
    while True:
        try:
            url_list = []
            url_set = get_url(work, target_page_no)
            for url in list(url_set):
                url_list.append(url)

            if len(url_list) > 0:
                kkconn.kafka_producer(url_list, work)
                current_url_count += len(url_list)
                print("Inserted {} URLS: {}, Current: {}".format(work["channel"], len(url_list), current_url_count))

            if current_url_count > limit_url_count:
                break

            target_page_no += 1

        except Exception as e:
            print(e)


def ins_get_url(work):
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


def twt_get_url(work):
    channel = work["channel"]
    work_group_no = work["work_group_no"]
    keyword = work["keyword"]
    start_date = work["start_date"]
    end_date = work["end_date"]

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





def collect_urls_by_inf_scorll(work):
    channel = work["channel"]
    if channel == "ins":
        ins_get_url(work)

    if channel == "twt":
        twt_get_url(work)


if __name__ == "__main__":

    work_list = [
        # {
        #     "channel": "dna",
        #     "keyword": "코로나 백신",
        #     "start_date": "2021-09-01",
        #     "end_date": "2021-09-30",
        #     "work_type": "collect_url",
        #     "work_group_no": 2,
        # },
        # {
        #     "channel": "nav",
        #     "keyword": "코로나 백신",
        #     "start_date": "2021-09-01",
        #     "end_date": "2021-09-30",
        #     "work_type": "collect_url",
        #     "work_group_no": 2,
        # },
        # {
        #     "channel": "twt",
        #     "keyword": "코로나 백신",
        #     "start_date": "2021-09-01",
        #     "end_date": "2021-09-30",
        #     "work_type": "collect_url",
        #     "work_group_no": 2,
        # },
        {
            "channel": "ins",
            "keyword": "코로나 백신",
            "start_date": "2021-09-01",
            "end_date": "2021-09-30",
            "work_type": "collect_url",
            "work_group_no": 2,
        }

    ]


    # print(work_list)
    # exit()

    for work in work_list:

        if work["channel"] == "ins":
            collect_urls(work)
            continue

        date_list = date_range("2021-09-01", "2021-09-30")
        for date in date_list:
            work["start_date"] = date
            work["end_date"] = date
            collect_urls(work)

# class Collector:
#
#     def __init__(self):
#         self.conf = cfg.get_config(path=dir.config_path)
#         self.chromeDriver = cfg.get_chrome_driver(config_path=dir.config_path)


# else:
# Isnert 후 바로 웹 페이지 수집 시작
# self.collect_urls3(work)


# def extract_texts(self, works):
#     work_type = "extract_text"
#     print(work_type)
#
#     for work in works:
#         prl.stop_procs(work)
#
#     p_count = 4
#     conf = cfg.get_config(path=dir.config_path)
#     for work in works:
#         channel = work["channel"]
#         keyword = work["keyword"]
#         work_group_no = work["work_group_no"]
#         work_no = work["work_no"]
#
#         target_path = conf["storage"]["save_dir"] + channel + '/'
#         file_list = [file for file in os.listdir(target_path) if ".html" in file]
#         total_file_count = len(file_list)
#         finished_file_count = Value('i', 0)
#         unit_count = int(len(file_list) / p_count)
#         remain_count = len(file_list) % p_count
#
#         ei = 0
#         for i in range(0, p_count):
#             si = unit_count * i
#             ei = unit_count * (i + 1)
#
#             prl.add_proc(work, Process(target=self.extract_feature, args=(channel, target_path, file_list[si:ei],
#                                                                           finished_file_count, total_file_count,
#                                                                           keyword, work_group_no, work_no)))
#
#         if remain_count > 0:
#             si = ei
#             ei = ei + remain_count
#             prl.add_proc(work, Process(target=self.extract_feature, args=(channel, target_path, file_list[si:ei],
#                                                                           finished_file_count, total_file_count,
#                                                                           keyword, work_group_no, work_no)))
#
#     prl.start_procs(work_type)

# def extract_feature(self, channel, target_path, file_list, finished_file_count, total_file_count, keyword, work_group_no, work_no):
#     tfe.create_doc_text_blocks(channel, target_path, file_list, finished_file_count, total_file_count, keyword, work_group_no, work_no)
#     # DBHandler().map_reduce(channel, "text", db_name="whateverdot", collection_name="docs")
#
#
# def extract_contents(self, works):
#
#     work_type = "extract_content"
#     print(work_type)
#
#     for work in works:
#         prl.stop_procs(work)
#
#     dbh = DBHandler()
#     zhpk = ZHPickle()
#     for work in works:
#         work_group_no = work["work_group_no"]
#         work_no = work["work_no"]
#         channel = work["channel"]
#         if channel == "nav":
#             continue
#
#         # 본문 부모 태그 경로 호출
#         # 학습된 {텍스트:순위} 딕셔너리 가져오기
#         dy1_ptp = zhpk.load("./modules/eda/statics_result/pickles/" + channel + "_y1_ptp_list.pickle")
#         text_rank_dct = zhpk.load("./modules/eda/statics_result/pickles/" + channel + "_text_rank_dct.pickle")
#
#         # DB에서 대상 피처 가져오기 Pandas DataFrame 만들기
#         # target_ds에 freq_rank 붙이기기
#         target_ds = dbh.find_item({"work_group_no": work_group_no, "work_no": work_no}, db_name="whateverdot", collection_name="docs")
#         zhpd = ZHPandas()
#         text_list = []
#         ptp_list = []
#         for d in target_ds:
#             text_list.append(d["text"])
#             ptp_list.append(d["ptp"])
#
#         target_ds = zhpd.create_data_frame_to_dict({
#             "text": text_list,
#             "ptp": ptp_list
#         })
#
#         target_rank_list = []
#         for i in range(len(target_ds)):
#             text = target_ds.loc[i, "text"]
#             target_rank_list.append(1 if text_rank_dct.get(text) is None else text_rank_dct[text])
#
#         df_rank_list = pd.DataFrame(target_rank_list, columns=["freq_rank"])
#         df_added_rank = pd.concat([target_ds, df_rank_list], axis=1)
#
#         # 본문 모 태그 경로로 거르기 Pandas ["text", "ptp"]
#         result = df_added_rank.query("ptp in " + str(dy1_ptp))
#
#         # freq_nav = 200
#         # freq_jna = 4
#
#         result = result[result.freq_rank <= 4].reset_index()
#
#         data_list = []
#         for index in range(len(result)):
#             print(result.loc[index, ["text", "ptp"]])
#             data_list.append({"work_group_no": work_group_no, "work_no": work_no, "text": result.loc[index, "text"]})
#
#         dbh.insert_item_many(data_list, db_name="whateverdot", collection_name="contents")
#         print("Inserted {} - {} contents".format(channel, len(data_list)))


# if __name__ == "__main__":
# 
#     dbh = DBHandler()
#     zhpd = ZHPandas()
# collector = Collector()
#
# target_ds = dbh.find_item({"work_group_no": 9, "work_no": 49},
#                                   db_name="whateverdot", collection_name="docs")
# text_list = []
# ptp_list = []
# for d in target_ds:
#     text_list.append(d["text"])
#     ptp_list.append(d["ptp"])
#
# target_ds = zhpd.create_data_frame_to_dict({
#     "text": text_list,
#     "ptp": ptp_list
# })
# print(target_ds.head())
#
# zhpk = ZHPickle()
# target_rank_list = []
# dy1_ptp = zhpk.load("../eda/statics_result/pickles/nav_y1_ptp_list.pickle")
#
# text_rank_dct = zhpk.load("../eda/statics_result/pickles/nav_text_rank_dct.pickle")
# for i in range(len(target_ds)):
#     text = target_ds.loc[i, "text"]
#     target_rank_list.append(1 if text_rank_dct.get(text) is None else text_rank_dct[text])
#
# df_rank_list = pd.DataFrame(target_rank_list, columns=["freq_rank"])
# df_added_rank = pd.concat([target_ds, df_rank_list], axis=1)
#
# # 본문 모 태그 경로로 거르기 Pandas ["text", "ptp"]
# result = df_added_rank.query("ptp in " + str(dy1_ptp))
# result = result[result.freq_rank <= 200].reset_index()
#
# data_list = []
# for index in range(len(result)):
#     data_list.append({"work_group_no": 9, "work_no": 49, "text": result.loc[index, "text"]})
#
# dbh.insert_item_many(data_list, db_name="whateverdot", collection_name="contents")
#
#
#
#
#
#
#
# {"work_group_no": work_group_no, "work_no": work_no, "text": result.loc[index, "text"]}
#     print(result.text)

# collector.migrate_labeling_data()
# work_list2 = []
# work3 = {
#     "channel": "nav",
#     "keyword": "코로나_백신",
#     "start_dt": "2021-01-01",
#     "end_dt": "2021-01-03",
#     "work_type": "extract_feature",
#     "work_group_no": 9,
#     "work_no": 49
# }
#
# work_list2.append(work3)
#
# collector = Collector()
# collector.extract_features(work_list2)

# time.sleep(30)
#
# work_list2 = []
# work2 = {}
# work2["channel"] = "nav"
# work2["keyword"] = "코로나_백신"
# work2["start_dt"] = "2021-01-01"
# work2["end_dt"] = "2021-01-03"
# work2["work_type"] = "collect_doc"
# work2["work_group_no"] = "11"
# work2["work_no"] = "100"
# work_list2.append(work2)
#
# work3 = {}
# work3["channel"] = "jna"
# work3["keyword"] = "코로나_백신"
# work3["start_dt"] = "2021-01-01"
# work3["end_dt"] = "2021-01-03"
# work3["work_type"] = "collect_doc"
# work3["work_group_no"] = "12"
# work3["work_no"] = "100"
# work_list2.append(work3)
#
# collector.collect_docs(work_list2)
