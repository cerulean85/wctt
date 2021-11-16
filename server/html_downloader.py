import json
import os
from multiprocessing import Process
from selenium.webdriver.common.keys import Keys

import config as cfg
import kkconn
import modules.collect.dir as dir
import time
from collections import Counter
import text_extractor as te
import text_preprocessor as tp

current_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
conf = cfg.get_config(path=current_path)
channel_spec = conf["channel_spec"]

def download(work, q):
    channel, work_group_no, keyword, date = \
        work["channel"], work["work_group_no"], work["keyword"], work["start_date"].replace('-', '')

    chromeDriver = cfg.get_chrome_driver(current_path)
    ins_login = False
    url_counter_dict = {}
    urls = []
    while True:
        url = q.get()
        urls.append(url)

        is_continue = True
        if len(urls) >= work["invoke_url_count"]:

            if channel == "ins" and not ins_login:
                ins_login = True
                cfg.ins_login(chromeDriver, dir.config_path)

            url_counter_dict[channel] = {
                "counter": Counter(),
                "work_group_no": work_group_no,
                "keyword": keyword,
                "date": date
            }

            url_counter_dict[channel]["counter"].update(urls)
            print(url_counter_dict)
            urls = []

            file_count = 0
            for channel, value in url_counter_dict.items():
                work_group_no = value["work_group_no"]
                keyword = value["keyword"]
                date = value["date"]
                dup_limit_count = conf[channel]["duplicated_limit_count"]

                for url_count in value["counter"].items():
                    url = url_count[0]
                    dup_count = url_count[1]

                    if dup_count > dup_limit_count:
                        print("Dup File Info: {}, {}, {}, {}, {}".
                              format(url, dup_count, work_group_no, keyword, date))
                        continue

                    switch_to_iframe = conf[channel]["switch_to_iframe"]
                    try:
                        chromeDriver.get(url)
                        time.sleep(1)
                    except Exception as e:
                        print("Can't collect {}, {}".format(url, e))
                        continue

                    if switch_to_iframe:
                        try:
                            iframe = chromeDriver.find_element_by_tag_name('iframe')
                            chromeDriver.switch_to.frame(iframe)
                            time.sleep(1)
                        except Exception as e:
                            print(e)
                            continue

                    limit_html_count = conf[channel]["limit_html_count"]
                    if channel in ["nav", "dna", "jna"] and file_count >= limit_html_count:
                        is_continue = False
                        break

                    work["source"] = str(chromeDriver.page_source)
                    work["index"] = file_count + 1

                    origin_save_path = work["csv_save_dir"] + '/origin'
                    if not os.path.isdir(origin_save_path):
                        os.makedirs(origin_save_path, exist_ok=True)

                    filename = '{}_{}.csv'.format(channel, date)
                    origin_save_path = origin_save_path + '/' + filename
                    work["filename"] = filename

                    extracted_text = te.extract(work)
                    if len(extracted_text) < 3:
                        continue

                    if not os.path.isfile(origin_save_path):
                        with open(origin_save_path, 'w', encoding="utf-8") as f:
                            f.write("text,keyword,date,channel\n")
                    else:
                        with open(origin_save_path, 'a', encoding="utf-8") as f:
                            f.write("{},{},{},{}\n".format(extracted_text, keyword, date, channel))
                        file_count += 1
                        print("[{} / {}] Added Text: {}".format(file_count, limit_html_count, extracted_text[0:50]))

                        p = Process(target=tp.preprocess_one, args=(work,))
                        p.start()

                    time.sleep(3)

                if not is_continue:
                    print("Preprocessing All...")
                    p = Process(target=tp.preprocess_all, args=(work,))
                    p.start()
                    break

            if not is_continue:
                chromeDriver.quit()
                break
