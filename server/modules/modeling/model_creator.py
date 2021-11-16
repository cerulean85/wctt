import os

import model_base as mb
# import models
from modules.zhbase.ZHPandas import ZHPandas
from modules.zhbase.ZHPickle import ZHPickle
import pandas as pd

# naver blog = 206
# tweeter = 166
# instagram = 151
# joongang = 149
# donga = 105

channel = "ins"
# path = "/data/train_data/{}/label/".format(channel)
path = "D:/__programming/__data2/ins/label/"
fp_list = [path + file for file in os.listdir(path)]

df = None
zhp = ZHPandas()
zhpk = ZHPickle()

filecount = 0
for filename in fp_list:
    if ".csv" not in filename:
        continue
    filecount += 1

fp_mergedDS = "../../models/{}/{}_mergedDS_{}.pickle".format(channel, channel, filecount)
fp_y1_ptp_list = "../../models/{}/{}_{}_y1_ptp_list.pickle".format(channel, channel, filecount)
fp_text_rank_dct = "../../models/{}/{}_{}_text_rank_dct.pickle".format(channel, channel, filecount)
fp_ptp_token_dct = "../../models/{}/{}_{}_ptp_token_dct.pickle".format(channel, channel, filecount)

def create_mergedDS(fp_mergedDS):
    res_df = None
    if os.path.isfile(fp_mergedDS):
        res_df = zhpk.load(fp_mergedDS)
    else:
        filecount = 0
        for filename in fp_list:
            if ".csv" not in filename:
                continue

            if res_df is None:
                res_df = zhp.read_csv(filename)
            else:
                __res_df = zhp.read_csv(filename)
                res_df = pd.concat([res_df, __res_df])

            filecount += 1
        zhpk.save(fp_mergedDS, res_df)
    return res_df

def create_y1_ptp_list(mergedDS, fp_y1_ptp_list):
    if os.path.isfile(fp_y1_ptp_list):
        res_df = zhpk.load(fp_y1_ptp_list)
    else:
        res_df = mergedDS.query("lb == 1").loc[:, "tags"]
        res_df = res_df.drop_duplicates()
        zhpk.save(fp_y1_ptp_list, list(res_df))
    return res_df

def create_text_rank_dict(mergedDS, fp_text_rank_dct):
    rank_dict = {}
    if os.path.isfile(fp_text_rank_dct):
        rank_dict = zhpk.load(fp_text_rank_dct)
    else:
        text_freq_dict = {}
        txt_list = mergedDS.loc[:, ["text"]].values
        for txt_arr in txt_list:
            txt = txt_arr[0]
            if text_freq_dict.get(txt) is None:
                text_freq_dict[txt] = 1
            else:
                text_freq_dict[txt] += 1

        sorted_dict_tuple = sorted(text_freq_dict.items(), key=lambda x: x[1])

        rank, prev_freq = 0, 0
        for item in sorted_dict_tuple:
            text, freq = item[0], item[1]
            if prev_freq < freq:
                rank += 1
                prev_freq = freq

            rank_dict[text] = rank

        zhpk.save(fp_text_rank_dct, rank_dict)
    return rank_dict

def create_ptp_token(mergedDS, fp_ptp_token_dct):
    ptp_token_dct = {}
    if os.path.isfile(fp_ptp_token_dct):
        ptp_token_dct = zhpk.load(fp_ptp_token_dct)
    else:
        ptp_list = mergedDS.loc[:, ["tags"]].values
        for ptp_arr in ptp_list:
            ptp = ptp_arr[0]
            if ptp_token_dct.get(ptp) is None:
                ptp_token_dct[ptp] = 1
            else:
                ptp_token_dct[ptp] += 1

        ptp_token_list = list(set(list(ptp_token_dct.keys())))
        print(ptp_token_list)
        for index in range(0, len(ptp_token_list)):
            ptp = ptp_token_list[index]
            ptp_token_dct[ptp] = (index + 1)
            # print(index + 1)
        zhpk.save(fp_ptp_token_dct, ptp_token_dct)

    return ptp_token_dct

mergedDS = create_mergedDS(fp_mergedDS).reset_index()
y1_ptp_list = create_y1_ptp_list(mergedDS, fp_y1_ptp_list)
rank_dict = create_text_rank_dict(mergedDS, fp_text_rank_dct)
ptp_token_dct = create_ptp_token(mergedDS, fp_ptp_token_dct)


# 출현빈도
text_list = []
x2_list = []
for index in range(0, len(mergedDS)):
    text = mergedDS.loc[index, "text"]
    text_list.append(text)
    x2_list.append(rank_dict[text])

x3_list = []
for index in range(0, len(mergedDS)):
    ptp = mergedDS.loc[index, "tags"]
    x3_list.append(ptp_token_dct[ptp])

x3_y_list = []
for ptp in y1_ptp_list:
    x3_y_list.append(ptp_token_dct[ptp])


print(len(x2_list), len(x3_list))

max_rank = max(list(rank_dict.values()))
answ_list = list(mergedDS.lb)
boundary_rank = 0
min_mse = 1.0
print("mse / rank / recall / precision / accuracy / fscore / fpr")
for rank in range(1, max_rank+1):
    pred_list = []
    for index in range(0, len(x2_list)):
        x2 = x2_list[index] # rank
        x3 = x3_list[index] # ptp
        label = 1 if (x2 <= rank) and (x3 in x3_y_list) else 0
        pred_list.append(label)

    _, _, _, _, recall, precision, accuracy, fscore, fpr = mb.fmeasure(pred_list, answ_list)
    vmse = mb.mse(pred_list, answ_list)
    print(
        "{:.5f} / {} / {:.3f} / {:.3f} / {:.3f} / {:.3f} / {:.3f}".
            format(vmse, rank, recall, precision, accuracy, fscore, fpr))

    if vmse <= min_mse:
        min_mse = vmse
        boundary_rank = rank

print("MSE:{}, Boundary Rank: {}".format(min_mse, boundary_rank))
for index in range(0, len(x2_list)):
    x2 = x2_list[index]  # rank
    x3 = x3_list[index]  # ptp
    if (x2 <= boundary_rank) and (x3 in x3_y_list):
        print(text_list[index])

    if index == 100:
        break

exit()
# print(mergedDS.tags)

# str_expr = "tags in " + str(y1_ptp_list)
str_expr = "lb == 1"
print(len(mergedDS.query(str_expr)))
# print(len(mergedDS))
# print(mergedDS[0:50])
# mergedDS.loc[0, "lb"] = 4
# print(mergedDS[0:1])

predict_list = []
for index in range(0, len(mergedDS)):
    ptp = mergedDS.loc[index, "tags"]
    if ptp in y1_ptp_list:
        print(ptp)
    # mergedDS.loc[index, "lb"] = 1 if ptp in y1_ptp_list else 0
print(len(mergedDS.query(str_expr)))
# ptp = mergedDS.loc[index, "tags"]
# print(ptp)
# for ptp in mergedDS.tags:
#     label = 1 if ptp in y1_ptp_list else 0
#     predict_list.append(label)
# print(predict_list[0:10])
# rank_dict = create_text_rank_dict(mergedDS, fp_text_rank_dct)
# print(rank_dict)
# ptp_list = list(mergedDS.x3.values)
# print(ptp_list[0:10])
# answer_list = list(mergedDS.y.values)
# print(answer_list[0:10])
# predict_list = []
# for ptp in ptp_list:
#     label = 1 if ptp in y1_ptp_list else 0
#     predict_list.append(label)
# print("Total Predicted: {}, Answer: {}".format(len(predict_list), len(answer_list)))
# TP, FP, TN, FN, recall, precision, accuracy, fscore, fpr = mb.fmeasure(predict_list, answer_list)
# print("[F-Score by PTP classification]")
# print("Recall: {}, Precision: {}, Accuracy: {}, F-Score: {}, FPR: {}".format(recall, precision, accuracy, fscore, fpr))


exit()

# dct = mb.load("/home/zhkim/github/ttawb/collector/models/nav/nav_5233_text_rank_dct.pickle")
# print(dct)
# exit()

# 모든 파일 읽어오기
# 텍스트 노드 추출하
from modules.extractor.ExtractorTextNode import ExtractorTextNode

def aggregate_text_rank(filepath, taf_rank_dict):
    wd = ExtractorTextNode()
    items = wd.create_text_node_list(filepath)
    for item in items:
        text = item["text"]
        taf_rank = 1 if taf_rank_dict.get(text) is None else taf_rank_dict.get(text)

mb.load_text_node("nav", 5233)
print(mb.merged_DS[0:10])
# txt_list = list(mb.merged_DS.x2.values)
# print(txt_list[0:50])
exit()


ptp_list = list(mb.merged_DS.x3.values)
print("PTPs: {}".format(ptp_list[0:10]))
print("Included PTP: {}, Unique PTP: {}".format(len(mb.y1_ptp_values), len(mb.uniq_case_1_ptp)))
answer_list = list(mb.merged_DS.y.values)
predict_list = []
for ptp in ptp_list:
    label = 1 if ptp in mb.uniq_case_1_ptp else 0
    predict_list.append(label)

print("Total Predicted: {}, Answer: {}".format(len(predict_list), len(answer_list)))
TP, FP, TN, FN, recall, precision, accuracy, fscore, fpr = mb.fmeasure(predict_list, answer_list)
print("[F-Score by PTP classification]")
print("Recall: {}, Precision: {}, Accuracy: {}, F-Score: {}, FPR: {}".format(recall, precision, accuracy, fscore, fpr))

mse, freq, freq_rank = mb.train_by_min_mse("x2")
mb.test("x2", freq)

mse, freq, freq_rank = mb.train_by_min_mse("x23")
mb.test("x23", freq)




# data = mb.load("statics_result/pickles/twt_3313_y0_ptp_values.pickle")
# print(data)