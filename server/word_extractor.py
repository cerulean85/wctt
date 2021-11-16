import os

import numpy as np

import config as cfg
import modules.collect.dir as dir
from modules.zhbase.ZHPandas import ZHPandas
from modules.zhbase.ZHPickle import ZHPickle

conf = cfg.get_config(path=dir.config_path)
html_save_dir = conf["storage"]["html_save_dir"]
csv_save_dir = conf["storage"]["csv_save_dir"]
model_path = dir.model_path
channel_spec = conf["channel_spec"]

zhpk = ZHPickle()
# reduced_text_dict = {}
# zhp = ZHPandas()
# for csv_save_group_dir, _, _ in os.walk(csv_save_dir):
#     for file in os.listdir(csv_save_group_dir):
#         if file[-4:] == ".csv":
#             filepath = csv_save_group_dir + '/' + file
#             df = zhp.read_csv(filepath)
#             text_list = list(df.loc[:, "text"].values)
#             for text in text_list:
#                 if reduced_text_dict.get(text) is None:
#                     reduced_text_dict[text] = 1
#                 else:
#                     reduced_text_dict[text] += 1
#

# zhpk.save("text_result.pickle", reduced_text_dict)
from konlpy.tag import Hannanum
tr = zhpk.load("text_result.pickle")
sorted_dict_tuple = sorted(tr.items(), key=lambda x: x[1], reverse=False)
text = ''
result_dict = {}
hannanum = Hannanum()
print(len(sorted_dict_tuple))
for tuple in sorted_dict_tuple[0:20000]:
    text = tuple[0]
    nouns = hannanum.nouns(text)
    for noun in nouns:
        if len(noun) > 1:
            if result_dict.get(noun) is None:
                result_dict[noun] = 1
            else:
                result_dict[noun] += 1

result = sorted(result_dict.items(), key=lambda x: x[1], reverse=False)
print(result[:])


#
# df = zhp.read_csv(filename)
