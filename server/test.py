import os
import time
import config as cfg
from modules.extractor.ExtractorTextNode import ExtractorTextNode
from modules.zhbase.ZHPickle import ZHPickle
from multiprocessing import Process, freeze_support, Queue
from datetime import datetime, timedelta


from eunjeon import Mecab
str = "freq_all.csv"
print(str.startswith("freq__", 0, 5))
exit()

mecab = Mecab()

f = open("test.csv", 'r', encoding='utf-8')
csv = f.read()
f.close()

print(csv)
morphs = mecab.nouns(csv)
print(morphs)
exit()



current_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
conf = cfg.get_config(path=current_path)
model_path = current_path + "/models/"
channel_spec = conf["channel_spec"]

def create_doc_text_blocks(work):
    target_path = work["target_file_path"]
    file_name = work["file_name"]
    content_ptp_list = work["model"]["content_ptp_list_path"]
    taf_rank_dict = work["model"]["taf_rank_path"]
    taf_boundary_rank = work["model"]["taf_boundary_rank"]

    str_text_nodes = ''
    try:
        mid_text_nodes = 'text,ptp,taf_rank\n'
        wd = ExtractorTextNode()
        items = wd.create_text_node_list(target_path + '/', file_name)
        for item in items:
            text = item["text"]
            ptp = item["ptp"]
            taf_rank = 1 if taf_rank_dict.get(text) is None else taf_rank_dict.get(text)
            mid_text_nodes += '{},{},{}\n'.format(text, ptp, taf_rank)
            if (ptp in content_ptp_list) and (taf_rank <= taf_boundary_rank)\
                    and len(text) > 2:
                str_text_nodes += '{} '.format(text)
    except Exception as e:
        print(e)

    return str_text_nodes

def extract(work):

    channel = work["channel"]
    work_group_no = work["work_group_no"]
    date_str = work["start_date"].replace('-', '')
    keyword = work["keyword"]
    html_save_dir = conf["storage"]["html_save_dir"] + str(work_group_no) + '/' + channel + '/' + date_str
    csv_save_dir = conf["storage"]["csv_save_dir"] + str(work_group_no) + '/' + channel
    models = {}

    if not os.path.isdir(csv_save_dir):
        os.makedirs(csv_save_dir, exist_ok=True)

    if models.get(channel) is None:
        if conf["model"].get(channel) is not None:
            content_ptp_list_path = model_path + channel + '/' + conf["model"][channel]["content_ptp_list"]
            taf_rank_path = model_path + channel + '/' + conf["model"][channel]["taf_rank"]
            taf_boundary_rank = conf["model"][channel]["taf_boundary_rank"]

            zhpk = ZHPickle()
            models[channel] = {
                "content_ptp_list_path": zhpk.load(content_ptp_list_path),
                "taf_rank_path": zhpk.load(taf_rank_path),
                "taf_boundary_rank": taf_boundary_rank
            }

        file_list = os.listdir(html_save_dir)
        file_list.sort(key=lambda x: (len(x), x))

        result = ''
        count = 1
        for file in file_list:
            tmp = file.split('.')
            tmp = tmp[0].split('_')
            channel, work_group_no, date, index = \
                tmp[0], int(tmp[1]), tmp[2], int(tmp[3])

            work = {
                "channel": channel,
                "work_group_no": work_group_no,
                "keyword": keyword,
                "date": date,
                "index": index,
                "target_file_path": html_save_dir,
                "file_name": file,
                "model": models[channel],
            }

            text = create_doc_text_blocks(work)
            count += 1
            if len(text) < 3:
                print("{}: is skipped.".format(count))
                continue
            contents = text + ",{},{},{}\n".format(keyword, date, channel)
            print("{}: {}".format(count, contents[0:100]))
            result += contents

        result = "text,keyword,date,channel\n" + result
        save_file_path = csv_save_dir + '/{}_{}_{}.csv'.format(channel, work_group_no, date_str)
        with open(save_file_path, "w", encoding="utf-8") as f:
            f.write(result)

def iter_extract(work, date_list):
    for date in date_list:
        work["start_date"] = date
        extract(work)

def date_range(start, end):
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end - start).days + 1)]
    return dates

if __name__ == "__main__":
    freeze_support()
    work = {
        "channel": "nav",
        "keyword": "코로나백신",
        "start_date": "2021-02-26",
        "end_date": "2021-02-26",
        "work_group_no": 20,
        "limit_url_count": conf["nav"]["limit_url_count"],
        "invoke_url_count": conf["nav"]["invoke_url_count"]
    }

    date_list = date_range("2021-09-01", "2021-10-31")
    date_list1 = date_list[0:40]
    date_list2 = date_list[40:80]
    date_list3 = date_list[80:124]

    procs = []
    procs.append(Process(target=iter_extract, args=(work, date_list1,)))
    procs.append(Process(target=iter_extract, args=(work, date_list2,)))
    procs.append(Process(target=iter_extract, args=(work, date_list3,)))
    for p in procs:
        p.start()

    # extract(work)


# def work():
#     conf = cfg.get_config(path=current_path)
#     html_save_dir = conf["storage"]["html_save_dir"]
#     csv_save_dir = conf["storage"]["csv_save_dir"]
#     model_path = current_path + "/models/"
#     channel_spec = conf["channel_spec"]
#
#     models = {}
#     zhpk = ZHPickle()
#     for channel in channel_spec:
#         if models.get(channel) is None:
#             if conf["model"].get(channel) is not None:
#                 content_ptp_list_path = model_path + channel + '/' + conf["model"][channel]["content_ptp_list"]
#                 taf_rank_path = model_path + channel + '/' + conf["model"][channel]["taf_rank"]
#                 taf_boundary_rank = conf["model"][channel]["taf_boundary_rank"]
#
#                 models[channel] = {
#                     "content_ptp_list_path": zhpk.load(content_ptp_list_path),
#                     "taf_rank_path": zhpk.load(taf_rank_path),
#                     "taf_boundary_rank": taf_boundary_rank
#                 }
#
#     last_index_check = {}
#     d = []
#     while True:
#         for html_save_group_dir, _, _ in os.walk(html_save_dir):
#             if html_save_dir == html_save_group_dir:
#                 continue
#
#             for html_save_channel_path, _, _ in os.walk(html_save_group_dir):
#                 if html_save_group_dir == html_save_channel_path:
#                     continue
#
#                 if len(os.listdir(html_save_channel_path)) > 0:
#                     if last_index_check.get(html_save_channel_path) is None:
#                         last_index_check[html_save_channel_path] = 0
#
#                 file_list = os.listdir(html_save_channel_path)
#                 file_list.sort(key=lambda x: (len(x), x))
#
#                 for file in file_list:
#                     tmp = file.split('.')
#                     tmp = tmp[0].split('_')
#                     channel = tmp[0]
#                     work_group_no = tmp[1]
#                     date = tmp[2]
#                     index = tmp[3]
#                     if last_index_check[html_save_channel_path] < index:
#                         last_index_check[html_save_channel_path] = index
#                         d.append(index)
#                         work = {
#                             "channel": channel,
#                             "work_group_no": work_group_no,
#                             "keyword": keyword,
#                             "date": date,
#                             "index": index,
#                             "target_file_path": html_save_channel_path,
#                             "file_name": file,
#                             "model": models[channel],
#                             "save_file_path": cfg.get_save_dir(csv_save_dir, work_group_no, channel) +
#                                               cfg.get_save_filename(channel, work_group_no, keyword, date, index, "csv")
#                         }
#
#                         create_doc_text_blocks(work)
#         time.sleep(5)


# import os
# import time
#
# import pandas as pd
#
# import config as cfg
# import modules.collect.dir as dir
# from modules.zhbase.ZHPandas import ZHPandas
#
# pd.set_option("display.max_rows", None)
#
# conf = cfg.get_config(path=dir.config_path)
# csv_save_dir = conf["storage"]["csv_save_dir"] + "/4/nav/"
#
# zhp = ZHPandas()
# count = 0
# for file in os.listdir(csv_save_dir):
#     if not ".csvf" in file:
#         txt = zhp.read_csv(csv_save_dir + file)
#         print("Dir:", csv_save_dir + file, "Count:", count)
#         print(txt[0:50])
#         time.sleep(3)
#         count += 1

# import url_collector
# from datetime import datetime, timedelta
#
# def date_range(start, end):
#     start = datetime.strptime(start, "%Y-%m-%d")
#     end = datetime.strptime(end, "%Y-%m-%d")
#     dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end-start).days+1)]
#     return dates


# if __name__ == "__main__":


# for

# work_list = [{
#         "channel": "nav",
#         "keyword": "코로나",
#         "start_date": "2021-09-26",
#         "end_date": "2021-09-28",
#         "work_type": "collect_url",
#         "work_group_no": 9,
#         "work_no": 1
#     }]
#
# url_collector.collect_urls(work_list)

# import os
# import pandas as pd
#
# from modules.extractor.TFAnaly import TFAnaly
# from modules.extractor.TFPreProc import TFPreProc
# from modules.extractor.TFWebDoc import TFWebDoc
# from modules.zhbase.ZHPandas import ZHPandas
# from modules.zhbase.ZHPickle import ZHPickle
#
# if __name__ == '__main__':
#
#     # tfp = TFPreProc()
#     # for index in range(1):
#     #     no = index + 1
#     #     tfw = TFWebDoc()
#     #     tfw.test_create_text_blocks("jna", "./jna_test/", "jna_web_doc_{}.html".format(no), "코로나")
#     #
#     #     for tb in tfw.get_tb_arr():
#     #         print(tb.get_parent_tags_pattern())
#     # print(tfw.get_tb_arr())
#     # dom = tfp.create_dom("./jna_test/jna_web_doc_1.html")
#     # print(dom)
#
#     zhpk = ZHPickle()
#     # df = zhpk.load("./modules/eda/dataset/jna_df.pickle")
#     # print(len(df))
#
#     # zhp = ZHPandas()
#     # tfa = TFAnaly()
#     # features_df = zhp.create_data_frame_to_dict(tfa.get_context_feature(df))
#     # zhpk.save("./modules/eda/dataset/jna_merged_DS.pickle", features_df)
#     # print(features_df.head())
#
#     df = zhpk.load("D:/__programming/whateverdot/collector/modules/eda/dataset/jna_merged_3201_DS.pickle")
#     # df[df.x12 == "html/body/div/div/div/div/div/div/div"].y = 0
#     # df[df.x12 == "html/body/div/div/div/div/div/div/div"].y = 0
#     # d = df[(df.x12 == "html/body/div/div/div/div/div/div/div") & (df.y == 1)]
#
#     remove_ptps = [
#         'html/body/div/div/div/div/div/div/a',
#         'html/body/div/div/div/div/div/div/div/div/div/a',
#         'html/body/div/div/div/div/div',
#         'html/body/div/div/div/div/div/div/div/div/h2',
#         'html/body/div/div/div/div/div/div/div/div/p/span',
#         'html/body/div/div/div/div/div/div/div/div/h3',
#         'html/body/div/div/div/div/div/div/div/dl/dd/span/strong'
#         # 'html/body/div/div/div/div/div/div/div'
#     ]
#
#     add_ptps = [
#         'html/body/div/div/div/div/div/div/div/ul/li/a'
#     ]
#
#     for ptp in remove_ptps:
#         df.loc[(df.x12 == ptp), 'y'] = 0
#
#     for ptp in add_ptps:
#         df.loc[(df.x12 == ptp), 'y'] = 1
#
#     print(len(df.loc[(df.x12 == 'html/body/div/div/div/div/div/div/div') & (df.y == 0)]),
#           len(df.loc[(df.x12 == 'html/body/div/div/div/div/div/div/div') & (df.y == 1)]))
#     # exit()
#
#     texts = []
#     ddf = df.loc[((df.x12 == 'html/body/div/div/div/div/div/div/div') & (df.y == 0))].x11.tolist()
#
#     candidate_texts = []
#     texts = list(set(ddf))
#     for text in texts:
#         if not ("입력" in text) and not ("수정" in text):
#             candidate_texts.append(text)
#
#     count = 0
#     index_list = df.index[(df.x12 == 'html/body/div/div/div/div/div/div/div')].tolist()
#     for index in index_list:
#         d = df.loc[index, ["x11", "x12", 'y']]
#         df.loc[index, 'y'] = 0 if d.x11 in candidate_texts else 1
#
#         if count % 3000 == 0:
#             print(count, '/', len(index_list),
#                   len(df.loc[(df.x12 == 'html/body/div/div/div/div/div/div/div') & (df.y == 0)]),
#                     len(df.loc[(df.x12 == 'html/body/div/div/div/div/div/div/div') & (df.y == 1)]))
#
#         count += 1
#
#     print(count, '/', len(index_list),
#           len(df.loc[(df.x12 == 'html/body/div/div/div/div/div/div/div') & (df.y == 0)]),
#           len(df.loc[(df.x12 == 'html/body/div/div/div/div/div/div/div') & (df.y == 1)]))
#
#     count = 0
#     index_list = df.index[(df.x12 == 'html/body/div/div/div/div/div/div')].tolist()
#     for index in index_list:
#         d = df.loc[index, ["x11", "x12", 'y']]
#         if len(d.x11) <= 12:
#             df.loc[index, 'y'] = 0
#
#         if count % 3000 == 0:
#             print(count, '/', len(index_list),
#                   len(df.loc[(df.x12 == 'html/body/div/div/div/div/div/div') & (df.y == 0)]),
#                     len(df.loc[(df.x12 == 'html/body/div/div/div/div/div/div') & (df.y == 1)]))
#
#         count += 1
#
#     print(count, '/', len(index_list),
#           len(df.loc[(df.x12 == 'html/body/div/div/div/div/div/div') & (df.y == 0)]),
#           len(df.loc[(df.x12 == 'html/body/div/div/div/div/div/div') & (df.y == 1)]))
#     zhpk.save("D:/__programming/whateverdot/collector/modules/eda/dataset/jna_merged_3201_DS.pickle", df)
#
#
#     # for text in candidate_texts:
#     #     df.loc[(df.x12 == 'html/body/div/div/div/div/div/div/div') & (df.x11 == text), 'y'] = 1
#
#     # print(len(df.query("x11 in " + str(candidate_texts))))
#     # print(df.y == 1)
#     # df.query("x11 in " + str(candidate_texts)).y = 1
#     # print(df.query("x11 in " + str(candidate_texts)).y)
#     # print(df.query("x11 in " + str(candidate_texts)))
#     # print(df.loc[df.x11 in candidate_texts])
#     # df.loc[df.query("x11 in " + str(candidate_texts)), 'y'] = 1
#     # print(df[(df.x12 == 'html/body/div/div/div/div/div/div/a')].head())
#     # print(df[(df.x12 == 'html/body/div/div/div/div/div/div/div/div/div/a')].head())
#     # print(df[(df.x12 == 'html/body/div/div/div/div/div')].head())
#     # print(df.loc[((df.x12 == 'html/body/div/div/div/div/div/div/div') & (df.y == 0)), ["x11", "y"]])
#     # print(df[(df.x12 == 'html/body/div/div/div/div/div/div/div/div/h2')].head())
#     # print(df[(df.x12 == 'html/body/div/div/div/div/div/div/div/div/p/span')].head())
#     # print(df[(df.x12 == 'html/body/div/div/div/div/div/div/div/div/h3')].head())
#
#     # print(df[df.freq_rank])
#     #
#     # df = None
#     # zhp = ZHPandas()
#     # path = "D:/__programming/__data2/jna/label/"
#     # for file in os.listdir(path):
#     #     if ".csv" in file:
#     #         if df is None:
#     #             df = pd.read_csv(path + file)
#     #         else:
#     #             df = zhp.concat_row(df, pd.read_csv(path + file))
#     #
#     #         print(len(df))
