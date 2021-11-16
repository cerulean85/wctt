# import json
# import os
# from multiprocessing import Process
# from selenium.webdriver.common.keys import Keys
#
# import config as cfg
# import kkconn
# import modules.collect.dir as dir
# import time
# from collections import Counter
# import text_extractor as te
#
# current_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
# conf = cfg.get_config(path=current_path)
# channel_spec = conf["channel_spec"]
#
# def download(work, q):
#     channel = work["channel"]
#     work_group_no = work["work_group_no"]
#     keyword = work["keyword"]
#     date = work["start_date"]
#     # save_path = work["save_path"]
#     chromeDriver = cfg.get_chrome_driver(current_path)
#     ins_login = False
#     url_counter_dict = {}
#     urls = []
#     while True:
#         url = q.get()
#         urls.append(url)
#
#         is_continue = True
#         if len(urls) >= work["invoke_url_count"]:
#
#             if channel == "ins" and not ins_login:
#                 ins_login = True
#                 cfg.ins_login(chromeDriver, dir.config_path)
#
#             url_counter_dict[channel] = {
#                 "counter": Counter(),
#                 "work_group_no": work_group_no,
#                 "keyword": keyword,
#                 "date": date
#             }
#
#             url_counter_dict[channel]["counter"].update(urls)
#             print(url_counter_dict)
#             urls = []
#
#             for channel, value in url_counter_dict.items():
#                 work_group_no = value["work_group_no"]
#                 keyword = value["keyword"]
#                 date = value["date"]
#                 dup_limit_count = conf[channel]["duplicated_limit_count"]
#
#                 cfg.make_dir(work["html_save_dir"], work_group_no, channel_spec)
#                 cfg.make_dir(work["csv_save_dir"], work_group_no, channel_spec)
#
#                 file_count = 0
#                 for url_count in value["counter"].items():
#                     url = url_count[0]
#                     dup_count = url_count[1]
#
#                     if dup_count > dup_limit_count:
#                         print("Dup File Info: {}, {}, {}, {}, {}".
#                               format(url, dup_count, work_group_no, keyword, date))
#                         continue
#
#                     switch_to_iframe = conf[channel]["switch_to_iframe"]
#                     try:
#                         chromeDriver.get(url)
#                         time.sleep(1)
#                     except Exception as e:
#                         print(e)
#                         print("Can't collect {}".format(url))
#                         continue
#
#                     if switch_to_iframe:
#                         try:
#                             iframe = chromeDriver.find_element_by_tag_name('iframe')
#                             chromeDriver.switch_to.frame(iframe)
#                             time.sleep(1)
#                         except Exception as e:
#                             print(e)
#                             continue
#
#                     # html_save_path = work["html_save_dir"] + '/' + date.replace('-', '') + '/'
#                     # if not os.path.isdir(html_save_path):
#                     #     os.makedirs(html_save_path, exist_ok=True)
#
#                     # file_count = len(os.listdir(html_save_path))
#                     # print(html_save_path, file_count)
#
#                     limit_html_count = conf[channel]["limit_html_count"]
#                     if channel in ["nav", "dna", "jna"] and file_count == limit_html_count:
#                         is_continue = False
#                         break
#                     # filename = cfg.get_save_filename(channel, work_group_no, keyword, date, index + 1, "html")
#                     # save_file_path = html_save_path + filename
#                     # with open(save_file_path, "w", encoding="utf-8") as f:
#                     #     f.write(str(chromeDriver.page_source))
#
#                     work["source"] = str(chromeDriver.page_source)
#                     work["index"] = file_count + 1
#                     te.extract(work)
#                     file_count += 1
#                     time.sleep(5)
#
#                     # print('Written {}...'.format(save_file_path))
#
#                     csv_save_path = work["csv_save_dir"] + '/' + date.replace('-', '') + '/'
#                     if not os.path.isdir(csv_save_path):
#                         os.makedirs(csv_save_path, exist_ok=True)
#
#                 if not is_continue:
#                     break
#
#             if not is_continue:
#                 p = Process(target=te.extract, args=(work,))
#                 p.start()
#                 chromeDriver.quit()
#                 break
#         # records = consumer.poll(3000)
#         # for tp, record in records.items():
#         #
#         #     ins_login = False
#         #     url_counter_dict = {}
#         #     for item in record:
#         #         url_info = json.loads(str(item.value.decode('utf-8')))
#         #
#         #         channel = url_info["channel"]
#         #         if work_channel_type != channel:
#         #             continue
#         #
#         #         work_group_no = url_info["work_group_no"]
#         #         date = url_info["date"]
#         #         keyword = url_info["keyword"].replace("'", "")
#         #
#         #         if channel == "ins" and not ins_login:
#         #             ins_login = True
#         #             cfg.ins_login(chromeDriver, dir.config_path)
#         #
#         #         if url_counter_dict.get(channel) is None:
#         #             url_counter_dict[channel] = {
#         #                 "counter": Counter(),
#         #                 "work_group_no": work_group_no,
#         #                 "keyword": keyword,
#         #                 "date": date
#         #             }
#         #
#         #         url_counter_dict[channel]["counter"].update(url_info["urls"])
#         #
#         #     for channel, value in url_counter_dict.items():
#         #         work_group_no = value["work_group_no"]
#         #         keyword = value["keyword"]
#         #         date = value["date"]
#         #         dup_limit_count = conf[channel]["duplicated_limit_count"]
#         #
#         #         cfg.make_dir(html_save_dir, work_group_no, channel_spec)
#         #         cfg.make_dir(save_path, work_group_no, channel_spec)
#         #
#         #         for url_count in value["counter"].items():
#         #             url = url_count[0]
#         #             dup_count = url_count[1]
#         #
#         #             if dup_count > dup_limit_count:
#         #                 print("Dup File Info: {}, {}, {}, {}, {}".
#         #                       format(url, dup_count, work_group_no, keyword, date))
#         #                 continue
#         #
#         #             switch_to_iframe = conf[channel]["switch_to_iframe"]
#         #             try:
#         #                 chromeDriver.get(url)
#         #                 time.sleep(1)
#         #             except Exception as e:
#         #                 print(e)
#         #                 print("Can't collect {}".format(url))
#         #                 continue
#         #
#         #             if switch_to_iframe:
#         #                 try:
#         #                     iframe = chromeDriver.find_element_by_tag_name('iframe')
#         #                     chromeDriver.switch_to.frame(iframe)
#         #                     time.sleep(1)
#         #                 except Exception as e:
#         #                     print(e)
#         #                     continue
#         #
#         #             filepath = cfg.get_save_dir(html_save_dir, work_group_no, channel)
#         #             index = len(os.listdir(filepath))
#         #             filename = cfg.get_save_filename(channel, work_group_no, keyword, date, index + 1, "html")
#         #             save_file_path = filepath + filename
#         #
#         #             with open(save_file_path, "w", encoding="utf-8") as f:
#         #                 f.write(str(chromeDriver.page_source))
#         #
#         #             time.sleep(5)
#         #             print('Written {}...'.format(save_file_path))
#
#
# # if __name__ == "__main__":
# #     procs = []
# #     procs.append(Process(target=work, args=("ins",)))
# #     procs.append(Process(target=work, args=("twt",)))
# #     procs.append(Process(target=work, args=("nav",)))
# #     procs.append(Process(target=work, args=("dna",)))
# #     for proc in procs:
# #         proc.start()
#     # for record in records:
#     #     print(record.value)
#     # url_info = json.loads(str(message.value.decode('utf-8')))
#     # url_counter.update(url_info["urls"])
#     # for item in url_counter.items():
#     #     print(item[0], item[1], count)
#     # channels = []
#     # for message in consumer:
#     #     url_info = json.loads(str(message.value.decode('utf-8')))
#     #     url_counter.update(url_info["urls"])
#     #     for item in url_counter.items():
#     #         print(item[0], item[1], count)
#
#     # channels.append(url_info["channel"])
#     # print(url_info)
#     # url_info = zhp.create_data_frame_to_dict(url_info)
#     # print(url_info, count)
#     # print( url_info["channel"] + str(count))
#     # print(count)
#     # print(len(channels))
#     # channel = ""
#     # work_group_no, work_no = 0, 0
#     # url_objs = []
#     #
#     # conf = cfg.get_config(path=dir.config_path)
#     # file_path = conf["storage"]["save_dir"] + channel
#     # switch_to_iframe = conf[channel]["switch_to_iframe"]
#     # index = 0
#     # chromeDriver = cfg.get_chrome_driver(dir.config_path)
#     #
#     # for item in url_objs:
#     #     url = item["url"]
#     #     chromeDriver.get(url)
#     #
#     #     if switch_to_iframe:
#     #         try:
#     #             iframe = chromeDriver.find_element_by_tag_name('iframe')
#     #             chromeDriver.switch_to.frame(iframe)
#     #             time.sleep(1)
#     #         except Exception as e:
#     #             print(e)
#     #             continue
#     #
#     #     file_info = {
#     #         "channel": channel,
#     #         "source": chromeDriver.page_source,
#     #         "filepath": file_path,
#     #         "filename": channel + "_web_doc_" + str(work_group_no) + '_' + str(work_no) + '_' + str(index + 1)
#     #     }
#     #
#     #     with open(file_info["filepath"] + '/' + file_info["filename"], "w", encoding="utf-8") as f:
#     #         f.write(str(file_info["source"]) + ".html")
#     #     print('Written {}...'.format(file_info["filename"]))
#     #
#     #     time.sleep(conf[channel]["delay_time"])
#     #     index += 1
#     #
#     # chromeDriver.quit()
