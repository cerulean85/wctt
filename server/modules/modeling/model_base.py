import os.path
import pickle
import gzip
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle

save_folder = "./statics_result/"
prefix = ""
channel = ""
file_count, count_0, count_1 = 0, 0, 0
merged_DS, data = None, None
total_ds_count, total_ds_y0_count, total_ds_y1_count = 0, 0, 0
size_uniq_case_all_ptp, size_uniq_case_0_ptp, size_uniq_case_1_ptp, size_intersection = 0, 0, 0, 0
x_values, all_ptp_values, dup_ptp_values, y0_ptp_values, y1_ptp_values = [0], [0], [0], [0], [0]
eq_ptp_list, eq_ptp_txt_list = [], []
train_count, train_ds, test_ds = 0, None, None
freq_rank = []

def set_meta_info(m_channel, m_file_count):
    global channel, file_count, prefix
    channel, file_count = m_channel, m_file_count
    prefix = channel + "_" + str(file_count) + "_"

def clear():
    global file_count, count_0, count_1, merged_DS, data, total_ds_count, total_ds_y0_count, total_ds_y1_count, \
    size_uniq_case_all_ptp, size_uniq_case_0_ptp, size_uniq_case_1_ptp, size_intersection, \
    x_values, all_ptp_values, dup_ptp_values, y0_ptp_values, y1_ptp_values, eq_ptp_list, eq_ptp_txt_list

    file_count, count_0, count_1 = 0, 0, 0
    merged_DS, data = None, None
    total_ds_count, total_ds_y0_count, total_ds_y1_count = 0, 0, 0
    size_uniq_case_all_ptp, size_uniq_case_0_ptp, size_uniq_case_1_ptp, size_intersection = 0, 0, 0, 0
    x_values, all_ptp_values, dup_ptp_values, y0_ptp_values, y1_ptp_values = [0], [0], [0], [0], [0]
    eq_ptp_list, eq_ptp_txt_list = [], []

def load(filename, compress=False):
    global data
    if not compress:
        with open(filename, "rb") as f:
            data = pickle.load(f)
        return data

    else:
        with gzip.open(filename, "rb") as f:
            data = pickle.load(f)
        return data

def total_ds_detail():
    global total_ds_count, total_ds_y0_count, total_ds_y1_count, merged_DS
    merged_DS = load("pickles/" + channel + "_merged_" + str(file_count) + "_DS.pickle")

    total_ds_count, total_ds_y0_count, total_ds_y1_count = \
        len(merged_DS), len(merged_DS[merged_DS.y == 0]), len(merged_DS[merged_DS.y == 1])

    # print("Total DS: {}".format(total_ds_count))
    # print("Contents DS: {}".format(total_ds_y1_count))
    # print("Non Contents DS: {}".format(total_ds_y0_count))
    # print("Validation Total DS: {}".format(total_ds_y0_count + total_ds_y1_count))
    y0_rate = total_ds_y0_count / total_ds_count
    y1_rate = total_ds_y1_count / total_ds_count

    ratio = [y0_rate, y1_rate]
    labels = ['Non Contents', 'Contents']
    explode = [0, 0.10]
    plt.pie(ratio, autopct='%.1f%%', explode=explode)
    plt.savefig(save_folder + prefix + "imbalanced_circle.png")

    return total_ds_count, total_ds_y0_count, total_ds_y1_count

def duplicated_ptp_count(ds):
    global size_uniq_case_all_ptp, size_uniq_case_0_ptp, size_uniq_case_1_ptp, size_intersection,\
        uniq_case_all_ptp, uniq_case_0_ptp, uniq_case_1_ptp, uniq_case_0_ptp_txt, uniq_case_1_ptp_txt

    uniq_case_all_ptp = ds.x3.unique()
    case_0_ptp = ds[ds.y == 0].x3
    uniq_case_0_ptp = case_0_ptp.unique()
    case_0_ptp_txt = ds[ds.y == 0].x12
    uniq_case_0_ptp_txt = case_0_ptp_txt.unique()
    case_1_ptp = ds[ds.y == 1].x3
    uniq_case_1_ptp = case_1_ptp.unique()
    case_1_ptp_txt = ds[ds.y == 1].x12
    uniq_case_1_ptp_txt = case_1_ptp_txt.unique()

    size_uniq_case_all_ptp = len(uniq_case_all_ptp)
    size_uniq_case_0_ptp = len(uniq_case_0_ptp)
    size_uniq_case_1_ptp = len(uniq_case_1_ptp)
    size_intersection = size_uniq_case_0_ptp + size_uniq_case_1_ptp - size_uniq_case_all_ptp

    # print("Total PTP: {}".format(size_uniq_case_all_ptp))
    # print("Contents Dup PTP: {}".format(size_uniq_case_1_ptp))
    # print("Non Contents Dup PTP: {}".format(size_uniq_case_0_ptp))
    # print("Intersection PTP: {}".format(size_intersection))

    return size_uniq_case_all_ptp, size_uniq_case_0_ptp, size_uniq_case_1_ptp, size_intersection



def visualize_ptp_rate_detail():
    global x_values, all_ptp_values, dup_ptp_values, y0_ptp_values, y1_ptp_values, save_folder, prefix, channel

    plt.figure(figsize=(10, 3.5))
    plt.subplot(121)
    # plt.title("Channel-Joongang")
    plt.plot(x_values, all_ptp_values, 'r', label="All PTP")
    plt.plot(x_values, y0_ptp_values, 'b--', label="Non-Contents PTP")
    plt.plot(x_values, y1_ptp_values, 'm-.', label="Contents PTP")
    plt.xlabel("Web Samples")
    plt.ylabel("Parent Tag Path Count")
    plt.legend()

    plt.subplot(122)
    plt.plot(x_values, dup_ptp_values, label="Duplicated PTP")
    plt.xlabel("Web Samples")
    # plt.ylabel("Parent Tag Path Count")
    # plt.ylim(6, 1)
    if channel == "twt" or channel == "ins" or channel == "dna":
        # plt.yticks([0, 1])
    # if channel == "dna":
        plt.yticks([0, 1, 2])
    plt.legend()
    plt.savefig(save_folder + prefix + "multi_line_ptp.png")

def quick(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[0]
    arr = arr[1:len(arr)]
    left_arr = []
    right_arr = []
    for x in arr:
        if x < pivot:
            left_arr.append(x)
        else:
            right_arr.append(x)

    left_arr = quick(left_arr)
    right_arr = quick(right_arr)

    left_arr.append(pivot)
    return left_arr + right_arr

def duplicated_ptp_detail():
    global uniq_case_all_ptp, uniq_case_0_ptp, uniq_case_1_ptp, uniq_case_0_ptp_txt, uniq_case_1_ptp_txt, merged_DS, \
    count_0, count_1, eq_ptp_list, eq_ptp_txt_list

    # 중복되는 PTP 확인하기
    for i in range(len(uniq_case_1_ptp)):
        for j in range(len(uniq_case_0_ptp)):
            if uniq_case_1_ptp[i] == uniq_case_0_ptp[j]:
                eq_ptp_list.append(uniq_case_0_ptp[j])
                eq_ptp_txt_list.append(uniq_case_0_ptp_txt[j])

    eq_ptp_dict = {}
    for i in range(len(eq_ptp_list)):
        key = eq_ptp_list[i]
        value = eq_ptp_txt_list[i]
        eq_ptp_dict[key] = value

    eq_ptp_list = quick(eq_ptp_list)

    with open(save_folder + prefix + "duplicated_tag.csv", "w", encoding="utf-8") as f:
        f.write("Pattern No, Parent Tag Pattern\n")
        for i in range(len(eq_ptp_list)):
            key = eq_ptp_list[i]
            f.write("{},{}\n".format(eq_ptp_list[i], eq_ptp_dict[key]))
            print("{}: {}".format(eq_ptp_list[i], eq_ptp_dict[key]))

    count_0, count_1 = 0, 1
    for ptp in eq_ptp_list:
        #     print("======== {}번 PTP: {}개 ========".format(ptp, len(merged_DS[merged_DS.x3 == ptp])))
        result = merged_DS[merged_DS.x3 == ptp]
        count_0 += len(result[result.y == 0])
        count_1 += len(result[result.y == 1])

    # print(len(eq_ptp_list))
    # print("Label = 0인 중복 PTP 텍스트 노드 개수: {}".format(count_0))
    # print("Label = 1인 중복 PTP 텍스트 노드 개수: {}".format(count_1))
    return count_0, count_1

def visualize_text_freq(ds, text_freq_filename, text_freq_graph_filename):
    # merged_DS에서 x2(출현빈도)와 x11(텍스트) 추출
    ttds = ds.loc[:, ["x2", "x11"]]
    ttds = ttds.sort_values(by=["x2"], ascending=False)
    tfqset = {}

    for key in ttds.loc[:, "x2"].values:
        tfqset[key] = set([])

    for i in range(len(ttds)):
        key = ttds.loc[i, "x2"]
        text = ttds.loc[i, "x11"]
        tfqset[key].add(text)

    with open(text_freq_filename, "w", encoding="utf-8") as f:
        f.write("No,Freq,Text\n")
        no = 1
        for item in tfqset.items():
            freq = item[0]
            for text in item[1]:
                f.write("{}, {},{}\n".format(no, freq, text))
                no += 1

    x_values = tfqset.keys()
    y_values = [len(values) for values in tfqset.values()]
    plt.figure(figsize=(12, 3.5))
    plt.subplot(121)
    plt.plot(x_values, y_values, 'r')
    plt.xlabel("Text Frequency")
    plt.ylabel("Text Count")
    #     plt.xticks([1, 2000, 4000, 6000, 8000, 10000])
    #     plt.yticks([1, 50000, 100000, 150000, 200000, 250000, 300000])

    # rank, log scale
    x_values = [index for index in range(len(x_values), 0, -1)]
    y_values = np.log(y_values)
    plt.subplot(122)
    plt.plot(x_values, y_values, 'r')
    plt.xlabel("Text Frequency Rank")
    plt.ylabel("Text Count (Log)")
    #     plt.xticks([1, 50, 100, 150, 200, 250, 300, 350])

    plt.savefig(text_freq_graph_filename)

def visualize_duplicated_label_prob_total():
    global count_0, count_1, total_ds_y0_count, total_ds_y1_count

    x_values = [0, 1]
    y_values_total = [total_ds_y0_count, total_ds_y1_count]
    y_values_ptp = [count_0, count_1]
    y_values = [count_0 / (count_0 + count_1), count_1 / (count_0 + count_1)]

    topics = ["No Contents(0)", "Contents(1)"]
    count = len(topics)

    def create_x(t, w, n, d):
        return [t * x + w * n for x in range(d)]

    value_a_x = create_x(2, 0.8, 1, count)
    value_b_x = create_x(2, 0.8, 2, count)
    ax = plt.subplot()
    ax.bar(value_a_x, y_values_ptp, label="Duplicated PTP")
    ax.bar(value_b_x, y_values_total, label="All PTP")
    # # plt.ylim(0, 1)
    middle_x = [(a + b) / 2 for (a, b) in zip(value_a_x, value_b_x)]
    ax.set_xticks(middle_x)
    ax.set_xticklabels(topics)
    plt.legend()
    plt.savefig(save_folder + prefix + "duplicated_label_prob_total.png")


def visualize_duplicated_label_prob_total_pie():
    global count_0, count_1, total_ds_y0_count, total_ds_y1_count

    x_values = [0, 1]
    y_values_total = [total_ds_y0_count, total_ds_y1_count]
    y_values_ptp = [count_0, count_1]
    # y_values = [count_0 / (count_0 + count_1), count_1 / (count_0 + count_1)]

    print(count_0, count_1, y_values_ptp, y_values_total)

    plt.pie([1,2])
    plt.show()

    # topics = ["No Contents(0)", "Contents(1)"]
    # count = len(topics)
    #
    # def create_x(t, w, n, d):
    #     return [t * x + w * n for x in range(d)]
    #
    # value_a_x = create_x(2, 0.8, 1, count)
    # value_b_x = create_x(2, 0.8, 2, count)
    # ax = plt.subplot()
    # ax.bar(value_a_x, y_values_ptp)
    # ax.bar(value_b_x, y_values_total)
    # # # plt.ylim(0, 1)
    # middle_x = [(a + b) / 2 for (a, b) in zip(value_a_x, value_b_x)]
    # ax.set_xticks(middle_x)
    # ax.set_xticklabels(topics)
    # plt.savefig(save_folder + prefix + "duplicated_label_prob_total_pie.png")


def duplicated_ptp_text_detail():
    global eq_ptp_list, merged_DS
    pd.set_option('display.max_row', len(merged_DS))

    for ptp in eq_ptp_list:
        #     print("======== {}번 PTP: {}개 ========".format(ptp, len(merged_DS[merged_DS.x3 == ptp])))
        result = merged_DS[merged_DS.x3 == ptp]
        print(result[result.y == 0].x11)

def mse(pred_lb_list, answ_lb_list):
    n = len(pred_lb_list)

    sumv = 0
    for i in range(n):
        ans, prd = answ_lb_list[i], pred_lb_list[i]
        v = ans - prd
        sumv += v * v

    return sumv / n


def fmeasure(pred_lb_list, answ_lb_list):
    TP, FP, TN, FN = 0, 0, 0, 0
    for i in range(len(pred_lb_list)):
        p, a = pred_lb_list[i], answ_lb_list[i]
        if a == 1 and p == 1:
            TP += 1

        if a == 0 and p == 0:
            TN += 1

        if a == 1 and p == 0:
            FN += 1

        if a == 0 and p == 1:
            FP += 1
    # print(TP, FP, TN, FN)

    b = (TP + FN)
    Recall = 0 if b == 0 else (TP / b)

    b = (TP + FP)
    Precision = 0 if b == 0 else (TP / b)

    b = (TP+TN+FN+FP)
    Accuracy = 0 if b == 0 else ((TP + TN) / b)

    b = (Recall + Precision)
    Fscore = 0 if b == 0 else (2 * Recall * Precision / b)

    b = (TP + FP)
    FPR = 0 if b == 0 else (FP / b)
    # 0, 1, 2, 3, 4, 5, 6, 7, 8
    return TP, FP, TN, FN, Recall, Precision, Accuracy, Fscore, FPR

def load(filename):
    with open(filename, "rb") as f:
        data = pickle.load(f)
    return data

def save(filename, data):
    with open(filename, "wb") as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)


def ptp_rate_detail():
    global x_values, all_ptp_values, dup_ptp_values, y0_ptp_values, y1_ptp_values, merged_DS

    # 웹 페이지 개수에 따른 PTP 중복률 변화 그래프
    # 하고 싶은 말: 웹 페이지의 개수가 많아질수록 중복되는 PTP의 개수도 많아짐
    # PTP만으로는 수집할 수 있는 본문 텍스트가 있다고 할 수 있으니, 이를 보완하기 위한 다른 특징 필요
    unit_node_count = len(merged_DS) / file_count
    for size in range(0, len(merged_DS), 1000):
        x_values.append(size / unit_node_count)
        all_ptp_value, y0_ptp_value, y1_ptp_value, dup_ptp_value = duplicated_ptp_count(merged_DS[0:size])
        dup_ptp_values.append(dup_ptp_value)
        all_ptp_values.append(all_ptp_value)
        y0_ptp_values.append(y0_ptp_value)
        y1_ptp_values.append(y1_ptp_value)
        print("{}: {}, {}, {}, {}".format(size, all_ptp_value, y0_ptp_value, y1_ptp_value, dup_ptp_value))

    size = len(merged_DS)
    x_values.append(size / unit_node_count)
    all_ptp_value, y0_ptp_value, y1_ptp_value, dup_ptp_value = duplicated_ptp_count(merged_DS[0:size])
    dup_ptp_values.append(dup_ptp_value)
    all_ptp_values.append(all_ptp_value)
    y0_ptp_values.append(y0_ptp_value)
    y1_ptp_values.append(y1_ptp_value)
    print("{}: {}, {}, {}, {}".format(size, all_ptp_value, y0_ptp_value, y1_ptp_value, dup_ptp_value))
    print("END")


def load_ptp_values():
    global save_folder, prefix, ptp_values_file_list, x_values, all_ptp_values, dup_ptp_values, \
        y0_ptp_values, y1_ptp_values, merged_DS

    if not os.path.isfile(save_folder + "pickles/" + prefix + "merged_DS.pickle"):
        ptp_rate_detail()
        save(save_folder + "pickles/" + prefix + "x_values.pickle", x_values)
        save(save_folder + "pickles/" + prefix + "all_ptp_value.pickle", all_ptp_values)
        save(save_folder + "pickles/" + prefix + "dup_ptp_values.pickle", dup_ptp_values)
        save(save_folder + "pickles/" + prefix + "y0_ptp_values.pickle", y0_ptp_values)
        save(save_folder + "pickles/" + prefix + "y1_ptp_values.pickle", y1_ptp_values)
        save(save_folder + "pickles/" + prefix + "merged_DS.pickle", merged_DS)

    x_values = load(save_folder + "pickles/" + prefix + "x_values.pickle")
    all_ptp_values = load(save_folder + "pickles/" + prefix + "all_ptp_value.pickle")
    dup_ptp_values = load(save_folder + "pickles/" + prefix + "dup_ptp_values.pickle")
    y0_ptp_values = load(save_folder + "pickles/" + prefix + "y0_ptp_values.pickle")
    y1_ptp_values = load(save_folder + "pickles/" + prefix + "y1_ptp_values.pickle")
    merged_DS = load(save_folder + "pickles/" + prefix + "merged_DS.pickle")

    print("{}, {}, {}, {}".format(len(all_ptp_values), len(y0_ptp_values), len(y1_ptp_values), len(dup_ptp_values)))


def get_rank(target_freq):
    global freq_rank

    for rank in range(len(freq_rank)):
        freq = freq_rank[rank]
        if target_freq == freq:
            return rank + 1

    return 0


def load_text_node(channel_code, file_count_value):
    global channel, file_count, prefix, merged_DS, freq_rank, train_count, train_ds, test_ds

    clear()
    set_meta_info(channel_code, file_count_value)

    print("Meta Info:", channel, file_count, prefix)
    print("Total TextNode Detail (all/0/1):", total_ds_detail())
    print("Duplicated PTP Detail (all/0/1/dup):", duplicated_ptp_count(merged_DS))
    print("Duplicated PTP TextNode Detail (0/1):", duplicated_ptp_detail())
    load_ptp_values()

    y1_ds = merged_DS[merged_DS.y == 1]
    tmp_freq_rank = {}
    for freq in y1_ds.x2:
        if tmp_freq_rank.get(freq) is None:
            tmp_freq_rank[freq] = 1
        else:
            tmp_freq_rank[freq] += 1

    freq_rank = quick(list(tmp_freq_rank.keys()))
    print(len(freq_rank), len(y1_ds), len(merged_DS))

    train_count = len(merged_DS) * 0.8
    train_ds = merged_DS.loc[0:train_count, ["x2", "x3", "y"]]
    test_ds = merged_DS.loc[train_count:len(merged_DS), ["x2", "x3", "y"]]
    print(len(train_ds), len(test_ds))


def visualize_ptp_tf_detail():
    global merged_DS, save_folder, prefix
    ptp_rate_detail()
    visualize_ptp_rate_detail()
    # 어떤 출현빈도에 많은 텍스트가 분포하는지를 살펴봄
    visualize_text_freq(merged_DS,
                        save_folder + prefix + "text_freq.csv",
                        save_folder + prefix + "text_freq_graph.png")

    visualize_duplicated_label_prob_total()


def get_predict_freq_list(ds, t_freq, feature):
    predict_list = []
    if feature == "x2":
        predict_list = x2(ds, t_freq)
    elif feature == "x2x3":
        predict_list = x2x3(ds, t_freq)

    return predict_list

# 출현 빈도=1인 녀석을 1로 결정
def x2(ds, threshold):
    predict_list = []
    x2_list = list(ds.x2.values)
    for i in range(len(x2_list)):
        label = 0
        x2 = x2_list[i]
        if x2 <= threshold:
            label = 1

        predict_list.append(label)
    return predict_list

# 본문 PTP 중 중복되는 PTP만 골라서 출현 빈도=1인 녀석을 1로 결정
def x2x3(ds, threshold):
    global uniq_case_1_ptp, uniq_case_0_ptp

    predict_list = []
    x2_list = list(ds.x2.values)
    x3_list = list(ds.x3.values)
    for i in range(len(x2_list)):
        label = 0
        x2 = x2_list[i]
        x3 = x3_list[i]
        if x3 in uniq_case_1_ptp:
            if x3 in uniq_case_0_ptp:
                if x2 <= threshold:
                    label = 1
            else:
                label = 1

        predict_list.append(label)
    return predict_list

def train_by_min_mse(feature):
    global train_ds, freq_rank

    # freq_list = list(set(list(train_ds.x2.values)))
    answer_list = list(train_ds.y.values)

    min_freq = 0
    min_mse = 0

    print("mse / t_freq(rank) / recall / precision / accuracy / fscore / fpr")
    for index in range(len(freq_rank)):
        t_freq = freq_rank[index]
        predict_list = get_predict_freq_list(train_ds, t_freq, feature)

        vmse = mse(predict_list, answer_list)
        if index == 0 or vmse < min_mse:
            min_mse = vmse
            min_freq = t_freq

            _, _, _, _, recall, precision, accuracy, fscore, fpr = fmeasure(predict_list, answer_list)
            print(
                "{:.3f} / {}({}) / {:.3f} / {:.3f} / {:.3f} / {:.3f} / {:.3f}".format(min_mse, min_freq, get_rank(min_freq), recall,
                                                                             precision, accuracy,
                                                                             fscore, fpr))

    predict_list = get_predict_freq_list(train_ds, min_freq, feature)
    _, _, _, _, recall, precision, accuracy, fscore, fpr = fmeasure(predict_list, answer_list)


    print(
        "Max: {:.3f} / {}({}) / {:.3f} / {:.3f} / {:.3f} / {:.3f} / {:.3f}".format(min_mse, min_freq, get_rank(min_freq), recall, precision, accuracy,
                                                                     fscore, fpr))
    return min_mse, min_freq, get_rank(min_freq)

def train_by_max_fsocre(ds, feature):
    x_values, y_recall_values, y_precision_values = [], [], []
    y_accuracy_values, y_fscore_values, y_fpr_values = [], [], []
    freq_list = list(set(list(ds.x2.values)))
    answer_list = list(ds.y.values)
    max_index, max_score = 0, 0
    print("t_freq / recall / precision / accuracy / fscore / fpr")
    for index in range(len(freq_list)):
        t_freq = freq_list[index]
        predict_list = get_predict_freq_list(ds, t_freq, feature)

        _, _, _, _, recall, precision, accuracy, fscore, fpr = fmeasure(predict_list, answer_list)

        x_values.append(t_freq)
        y_recall_values.append(recall)
        y_precision_values.append(precision)
        y_accuracy_values.append(accuracy)
        y_fscore_values.append(fscore)
        y_fpr_values.append(fpr)

        if fscore >= max_score:
            max_score = fscore
            max_index = index

        print(
            "{} / {:.3f} / {:.3f} / {:.3f} / {:.3f} / {:.3f}".format(t_freq, recall, precision, accuracy, fscore, fpr))

    t_freq = freq_list[max_index]
    recall = y_recall_values[max_index]
    precision = y_precision_values[max_index]
    accuracy = y_accuracy_values[max_index]
    fscore = y_fscore_values[max_index]
    fpr = y_fpr_values[max_index]

    print("====================================================")
    print(
        "MAX: {} / {:.3f} / {:.3f} / {:.3f} / {:.3f} / {:.3f}".format(t_freq, recall, precision, accuracy, fscore, fpr))
    return t_freq


def test(feature, t_freq):
    global test_ds
    x_values, y_recall_values, y_precision_values = [], [], []
    y_accuracy_values, y_fscore_values, y_fpr_values = [], [], []
    # freq_list = list(set(list(ds.x2.values)))
    answer_list = list(test_ds.y.values)

    if feature == "x2":
        predict_list = x2(test_ds, t_freq)
    elif feature == "x2x3":
        predict_list = x2x3(test_ds, t_freq)

    _, _, _, _, recall, precision, accuracy, fscore, fpr = fmeasure(predict_list, answer_list)
    tfrank = get_rank(t_freq)

    print("t_freq / tf_rank / recall / precision / accuracy / fscore / fpr")
    print(
        "MAX: {} / {} / {:.3f} / {:.3f} / {:.3f} / {:.3f} / {:.3f}".format(t_freq, tfrank, recall, precision, accuracy,
                                                                           fscore, fpr))

    return predict_list