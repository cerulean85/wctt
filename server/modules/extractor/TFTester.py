import os

from modules.extractor.ExtractorFeature import ExtractorFeature
from modules.extractor.ExtractorTextNode import ExtractorTextNode
import numpy as np
import pandas as pd
from multiprocessing import Value, Process
from modules.extractor import ExtractorConfig as tfg
from modules.zhbase.ZHPandas import ZHPandas
from modules.zhbase.ZHPickle import ZHPickle

np.set_printoptions(threshold=np.inf, linewidth=np.inf)
pd.set_option('display.max_columns', None)  ## 모든 열을 출력한다.
pd.set_option('display.max_rows', None)  ## 모든 열을 출력한다.

def create_doc_text_blocks(target_path, file_list, finished_file_count, total_file_count):

    save_path = target_path + "nodes/"
    print(save_path)
    print(file_list)

    target_file_list = []

    if not os.path.isdir(save_path):
        os.makedirs(save_path, exist_ok=True)

    for file in file_list:
        if "html" in file:
            target_file_list.append(file)

    print(target_file_list)
    str_text_nodes = 'text,ptp,label\n'
    for file in target_file_list:
        try:
            wd = ExtractorTextNode()

            for text_node in wd.create_text_node_list(target_path, file):
                str_text_nodes += text_node["text"] + ',' + text_node["ptp"] + ',0\n'

            finished_file_count.value += 1

            with open(save_path + file.split('.')[0] + ".csv", "w", encoding="utf-8") as f:
                f.write(str_text_nodes)

            print("Written [{}] - [{}/{}] ...".format(file, finished_file_count.value, total_file_count))
        except Exception as e:
            print(e)


def extract_nodes(target_path, channel):
    target_path = target_path + channel + '/'
    file_list = [file for file in os.listdir(target_path) if ".html" in file]
    print(len(file_list))

    p_list = []
    total_file_count = len(file_list)
    finished_file_count = Value('i', 0)
    unit_count = int(len(file_list) / tfg.PROCESS_COUNT)
    remain_count = len(file_list) % tfg.PROCESS_COUNT

    ei = 0
    for i in range(0, tfg.PROCESS_COUNT):
        si = unit_count * i
        ei = unit_count * (i + 1)
        p_list.append(Process(target=create_doc_text_blocks, args=(target_path, file_list[si:ei], finished_file_count, total_file_count)))

    if remain_count > 0:
        si = ei
        ei = ei + remain_count
        p_list.append(Process(target=create_doc_text_blocks, args=(target_path, file_list[si:ei], finished_file_count, total_file_count)))

    for p in p_list:
        p.start()


def extract_features(target_path, channel):
    save_path = target_path + channel + "/features/"
    target_path = target_path + channel + "/nodes/"

    if not os.path.isdir(save_path):
        os.makedirs(save_path, exist_ok=True)

    file_list = [file for file in os.listdir(target_path) if ".csv" in file]

    zhp = ZHPandas()
    zhpk = ZHPickle()
    result = None
    for file in file_list:
        file = target_path + file
        if result is None:
            result = zhp.read_csv(file)
        else:
            result = zhp.concat_row(result, zhp.read_csv(file))

    extractor = ExtractorFeature()
    result = extractor.get_context_feature(result)
    result = zhp.create_data_frame_to_dict(result)
    zhpk.save(save_path + "features.pickle", result)


def extract_contents():
    pass


def read_features(target_path):
    zhpk = ZHPickle()
    return zhpk.load(target_path)


if __name__ == '__main__':
    # extract_nodes("D:/__programming/__data3/", "ins")

    pfile = "D:/__programming/jcoty/server/models/ins/ins_8664_y1_ptp_list.pickle"
    # pfile = "D:/__programming/jcoty/server/models/nav/nav_5233_y1_ptp_list.pickle"
    result = read_features(pfile)
    print(result)
    exit()
    zhpk = ZHPickle()
    result = zhpk.load(pfile)
    no_list = ["html/head"]
    # no_list = [
    #     "html/body/div/div/div/div/div/div/div/div/div/div/div/table/tbody/tr/td/div/div/div/div/div/p",
    #     "html/body/div/div/div/div/div/div/div/div/div/div/div/table/tbody/tr/td/div/div/h4"]
    _tt = []
    for tp in result:
        if tp in no_list:
            continue
        _tt.append(tp)
    result = _tt
    zhpk.save(pfile, result)
    print(result)

    # extract_features("D:/__programming/__data3/", "jna")
    # result = read_features("D:/__programming/__data3/jna/features/features.pickle")
    # print(result)
