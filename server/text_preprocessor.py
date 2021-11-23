import os
from collections import Counter
from math import log

import pandas as pd
from eunjeon import Mecab
from wordcloud import WordCloud
import matplotlib.pyplot as plt

from modules.zhbase.ZHPandas import ZHPandas
from tqdm import tqdm
from gensim.models import word2vec


def preprocess(work):
    mecab = Mecab()
    save_path = work["data_directory"] + '/csv/' + str(work["id"])
    f = open("./stopwords.txt", 'r', encoding="utf-8")
    stopwords = f.read().split('\n')[0:-2]
    f.close()

    files = os.listdir(save_path + '/origin')
    for file in files:
        # print(file)
        morphs = []
        txt_arr = pd.read_csv(save_path + '/origin/' + file)
        try:
            for txt in txt_arr.text:
                txt_morphs = mecab.nouns(txt)
                morphs = morphs + [text for text in txt_morphs if text not in stopwords and len(text) > 1]
                sentence = ''
                for word in txt_morphs:
                    if len(word) > 1 and word not in stopwords:
                        # print(word)
                        sentence += word + ' '

                if len(sentence) > 0:
                    ext_save_path = save_path + "/ext_{}.csv".format(work["id"])
                    if not os.path.isfile(ext_save_path):
                        with open(ext_save_path, 'w', encoding="CP949") as f:
                            f.write("morphs\n{}\n".format(sentence))
                    else:
                        with open(ext_save_path, 'a', encoding="CP949") as f:
                            f.write("{}\n".format(sentence))
        except:
            continue

def create_table(work):
    save_path = work["data_directory"] + '/csv/' + str(work["id"])
    f = open("./stopwords.txt", 'r', encoding="utf-8")
    stopwords = f.read().split('\n')[0:-2]
    f.close()

    target_preproc_file_path = save_path + '/ext_{}.csv'.format(work["id"])
    ext_tf_table_save_path = save_path + '/ext_tf_table.csv'
    ext_tf_coo_matrix_save_path = save_path + '/ext_coo_matrix.csv'

    morphs_by_docs = {}
    txt_arr = pd.read_csv(target_preproc_file_path, encoding="CP949")
    morphs_by_docs["morphs_all"] = []
    doc_count = 1
    for txt in tqdm(txt_arr.morphs, desc="Creating Morphs Dictionary"):
        morphs = txt.split(' ')

        morphs_by_docs[str(doc_count)] = {
            "morphs": morphs,
            "morphs_tf": dict(Counter(morphs))
        }

        morphs_by_docs["morphs_all"] = morphs_by_docs["morphs_all"] + \
                                       [morph for morph in morphs if morph not in stopwords and len(morph) > 1]

        doc_count += 1

    morphs_by_docs["morphs_all_tf"] = dict(Counter(morphs_by_docs["morphs_all"]))
    morphs_all_list = set(list(morphs_by_docs["morphs_all_tf"].keys()))

    if work["table_tf"]:
        print("Started to create TF Table.")

        contents = "word,freq\n"
        for morph in tqdm(morphs_by_docs["morphs_all_tf"].keys(), desc="Creating TF Table"):
            freq = morphs_by_docs["morphs_all_tf"][morph]
            contents += "{},{}\n".format(morph, freq)
        # for morph, freq in morphs_by_docs["morphs_all_tf"].items():
        #     contents += "{},{}\n".format(morph, freq)

        with open(ext_tf_table_save_path, 'w', encoding="CP949") as f:
            f.write(contents)

        print("Saved TF Table.")

    if work["table_tfidf"]:
        print("Started to create TF-IDF Table.")

        morphs_by_docs["morphs_all_df"] = {}
        for morph in morphs_all_list:
            count = 0

            for i in range(1, doc_count):
                if morph in list(morphs_by_docs[str(i)]["morphs_tf"].keys()):
                    count += 1
            morphs_by_docs["morphs_all_df"][morph] = count

        weight_save_path = save_path + "/weights"
        if not os.path.isdir(weight_save_path):
            os.makedirs(weight_save_path, exist_ok=True)

        for i in range(1, doc_count):
            morphs_tf_idf = {}
            for morph, tf in morphs_by_docs[str(i)]["morphs_tf"].items():
                if len(morph) == 0:
                    continue

                df = morphs_by_docs["morphs_all_df"][morph]
                idf = log(doc_count / (1 + df))
                morphs_tf_idf[morph] = '{:.4f}'.format(tf * idf)

            res = sorted(morphs_tf_idf.items(), key=(lambda x:x[1]), reverse=True)

            contents = "word,weight\n"
            for row in res:
                morph, freq = row[0], row[1]
                contents += "{},{}\n".format(morph, freq)

            weight_save_path = save_path + "/weights/doc_{}.csv".format(i)
            with open(weight_save_path, 'w', encoding="CP949") as f:
                f.write(contents)

            print("Saved TF-IDF Table.")


    if work["table_tcoo"]:
        print("Started to create Coo-matrix.")
        coo_matrix = {}
        for morph1 in morphs_all_list:
            coo_matrix[morph1] = [0 for _ in range(0, len(morphs_all_list))]

        morphs_all_index_list = {}
        index = 0
        for morph in list(morphs_all_list):
            morphs_all_index_list[morph] = index
            index += 1

        for i in range(1, doc_count):
            doc = morphs_by_docs[str(i)]["morphs_tf"]
            for morph1 in doc.keys():
                if len(morph1) > 0:
                    for morph2 in doc.keys():
                        if morph1 != morph2 and len(morph2) > 0:
                            index = morphs_all_index_list[morph2]
                            coo_matrix[morph1][index] += 1

        coo_df = pd.DataFrame(coo_matrix)
        rename_dct = {}
        index = 0
        for morph in morphs_all_list:
            rename_dct[index] = morph
            index += 1
            coo_df.rename(columns=rename_dct, index=rename_dct, inplace=True)

        coo_df.to_csv(ext_tf_coo_matrix_save_path, index=True, encoding="CP949")
        print("Saved Coo-matrix.")

        # for morph1 in morphs_all_list:
        #     for morph2 in morphs_all_list:
        #         if morph1 == morph2:
        #             continue
        #
        #
        #     for i in range(1, doc_count):
        #         for morph in morphs_by_docs[str(i)]["morphs_tf"].keys():



    exit()




    # xx_wc_save_dir = '{}/client/public/wordcloud/{}'.format(work["proj_directory"], work["work_group_no"])
    # if not os.path.isdir(xx_wc_save_dir):
    #     os.makedirs(xx_wc_save_dir, exist_ok=True)
    # wc_save_path = xx_wc_save_dir + '/wordcloud.png'
    files = os.listdir(save_path + '/origin')
    files_dictionary = {}

    # txt_arr = pd.read_csv(target_preproc_file_path)
    # for txt in txt_arr.text:
    #     txt_morphs = mecab.nouns(txt)
    #     noun_counter_by_docs = Counter(txt_morphs)
    #
    #     sentence = ''
    #     for word in txt_morphs:
    #         if len(word) > 1:
    #             sentence += word + ' '
    #
    #     ext_save_path = save_path + "/origin/xx_{}".format(file)
    #     if not os.path.isfile(ext_save_path):
    #         with open(ext_save_path, 'w', encoding="utf-8") as f:
    #             f.write("{}\n".format(sentence))
    #     else:
    #         with open(ext_save_path, 'a', encoding="utf-8") as f:
    #             f.write("{}\n".format(sentence))
    #
    #     files_dictionary[key]["morphs_by_docs"].append(txt_morphs)
    #     files_dictionary[key]["tf_by_docs"].append(noun_counter_by_docs)
    #
    #     morphs = morphs + [text for text in txt_morphs if text not in stopwords and len(text) > 1]


    # for file in files:
    #     if ".csv" in file and (not file.startswith("xx_", 0, 3)):
    #         dot_arr = file.split('.')
    #         # unbar_arr = dot_arr[0].split('_')
    #         # channel = unbar_arr[0]
    #         # wgid = unbar_arr[1]
    #         # ymd_date = unbar_arr[2][0:8]
    #         # key = ymd_date
    #         key = dot_arr[0]
    #         # print(key)
    #
    #         if files_dictionary.get(key) is None:
    #             files_dictionary[key] = {
    #                 "path": save_path + '/origin/' + file,
    #                 "morphs": []
    #             }
    #
    #         morphs = []
    #         files_dictionary[key]["morphs_by_docs"] = []
    #         files_dictionary[key]["tf_by_docs"] = []
    #         txt_arr = pd.read_csv(save_path + '/origin/' + file)
    #         for txt in txt_arr.text:
    #             txt_morphs = mecab.nouns(txt)
    #             noun_counter_by_docs = Counter(txt_morphs)
    #
    #             sentence = ''
    #             for word in txt_morphs:
    #                 if len(word) > 1:
    #                     sentence += word + ' '
    #
    #             ext_save_path = save_path + "/origin/xx_{}".format(file)
    #             if not os.path.isfile(ext_save_path):
    #                 with open(ext_save_path, 'w', encoding="utf-8") as f:
    #                     f.write("{}\n".format(sentence))
    #             else:
    #                 with open(ext_save_path, 'a', encoding="utf-8") as f:
    #                     f.write("{}\n".format(sentence))
    #
    #             files_dictionary[key]["morphs_by_docs"].append(txt_morphs)
    #             files_dictionary[key]["tf_by_docs"].append(noun_counter_by_docs)
    #
    #             morphs = morphs + [text for text in txt_morphs if text not in stopwords and len(text) > 1]
    #
    #         nouns_counter = Counter(morphs)
    #         files_dictionary[key]["morphs"] = morphs
    #         files_dictionary[key]["noun_counter"] = nouns_counter
    #
    # morphs = []
    # for key, item in files_dictionary.items():
    #     morphs = morphs + [text for text in item["morphs"] if text not in stopwords and len(text) > 1]
    #
    # # exit()
    #
    # # print(morphs)
    # # model = word2vec.Word2Vec(sentences=morphs, vector_size=100, window=5, min_count=5, workers=4, sg=0)
    # # print(model.wv.most_similar("코로나"))
    # # exit()
    #
    # nouns_counter = Counter(morphs)
    # top_nouns = dict(nouns_counter.most_common(200))
    # nouns_dict = top_nouns
    #
    # text_id, id_text = {}, {}
    # id = 0
    # for noun in nouns_dict:
    #     text_id[noun] = id
    #     id_text[id] = noun
    #     id += 1
    #
    # target_dict = {}
    # for id in id_text.keys():
    #     target_dict[id] = [0 for i in range(0, len(nouns_dict.keys()))]
    #
    # for key, item in files_dictionary.items():
    #     for n_key, count in item["noun_counter"].items():
    #         if nouns_dict.get(n_key) is not None:
    #             nouns_dict[n_key] += count
    #
    # if work["create_tf_table"]:
    #     rename_dct = {}
    #     index = 0
    #     for text in nouns_dict.keys():
    #         rename_dct[index] = text
    #         index += 1
    #
    #     df = pd.DataFrame({
    #         "word": nouns_dict.keys(),
    #         "count": nouns_dict.values()
    #     })
    #     df.to_csv(xx_tf_table_save_path, index=False)
    #     print("Saved: {}".format(xx_tf_table_save_path))
    #
    # if work["create_wordcloud"]:
    #     wordcloud = WordCloud(
    #         font_path="fonts/NanumGothic.ttf",
    #         width=800,
    #         height=800,
    #         background_color='white',
    #         max_font_size=200
    #     )
    #     wordcloud.generate_from_frequencies(top_nouns)
    #     plt.figure(figsize=(8, 8))  # 이미지 사이즈 지정
    #     plt.imshow(wordcloud, interpolation='lanczos')  # 이미지의 부드럽기 정도
    #     plt.axis('off')  # x y 축 숫자 제거
    #     plt.savefig(wc_save_path)
    #     print("Saved: {}".format(wc_save_path))
    #
    # nouns = list(text_id.keys())
    #
    # for key, item in files_dictionary.items():
    #     noun_counter = item["noun_counter"]
    #     doc_dict = dict(noun_counter)
    #
    #     for i in range(0, len(nouns)):
    #         noun_1 = nouns[i]
    #         j, k = i + 1, i + 1
    #         for j in range(k, len(nouns)):
    #             noun_2 = nouns[j]
    #             if doc_dict.get(noun_1) is not None and doc_dict.get(noun_2) is not None:
    #                 noun_1_index, noun_2_index = text_id[noun_1], text_id[noun_2]
    #                 target_dict[noun_1_index][noun_2_index] += 1
    #
    # if work["create_tf_coo_table"]:
    #     df = pd.DataFrame(target_dict)
    #
    #     rename_dct = {}
    #     index = 0
    #     for text in text_id.keys():
    #         rename_dct[index] = text
    #         index += 1
    #     df.rename(columns=rename_dct, index=rename_dct, inplace=True)
    #
    #     ndf = df.to_numpy()
    #     len(ndf)
    #     for i in range(0, len(ndf)):
    #         for j in range(0, len(ndf)):
    #             ndf[i][j] = ndf[j][i]
    #
    #     df = pd.DataFrame(ndf)
    #     df.rename(columns=rename_dct, index=rename_dct, inplace=True)
    #     df.to_csv(xx_tf_coo_matrix_save_path)
    #     print("Saved: {}".format(xx_tf_coo_matrix_save_path))
    #
    # if work["create_tf_idf_table"]:
    #     df_dict = {}
    #     docs_count = 0  # len(files_dictionary.keys())
    #     for noun in top_nouns.keys():
    #         df_dict[noun] = 0
    #         for key, item in files_dictionary.items():
    #             for doc in item["morphs_by_docs"]:
    #                 docs_count += 1
    #                 if noun in doc:
    #                     df_dict[noun] += 1
    #                     continue
    #     print("docs_count: {}".format(docs_count))
    #     for _, item in files_dictionary.items():
    #         item["tfidf_by_docs"] = []
    #         for doc_tf in item["tf_by_docs"]:
    #             doc_tfidf = []
    #             for df_key, df_value in df_dict.items():
    #                 tf = 0 if doc_tf.get(df_key) is None else doc_tf[df_key]
    #                 idf = log(docs_count / (1 + df_value))
    #                 doc_tfidf.append(tf * idf)
    #             item["tfidf_by_docs"].append(doc_tfidf)
    #
    #     zhp = ZHPandas()
    #     doc_index = 1
    #     tfidf_df = pd.DataFrame()
    #     for _, item in files_dictionary.items():
    #         for doc_tfidf in item["tfidf_by_docs"]:
    #             doc_id = "doc" + str(doc_index)
    #             df = zhp.create_data_frame_to_dict({doc_id: doc_tfidf})
    #             tfidf_df = zhp.concat_column(tfidf_df, df)
    #             doc_index += 1
    #
    #     rename_dct = {}
    #     index = 0
    #     for text in df_dict.keys():
    #         rename_dct[index] = text
    #         index += 1
    #     tfidf_df.rename(index=rename_dct, inplace=True)
    #     tfidf_df.to_csv(xx_tf_idf_table_save_path)
    #     print("Saved: {}".format(xx_tf_idf_table_save_path))



def preprocess_one(work):
    mecab = Mecab()
    save_path = "C:/Users/JHKim/data/csv" #work["csv_save_dir"]
    target_file = save_path + "/example30.csv" # work["filename"]
    f = open("./stopwords.txt", 'r', encoding="utf-8")
    stopwords = f.read().split('\n')[0:-2]
    f.close()

    print(stopwords)

    files_dictionary = {}
    # freq_save_path = save_path + '/result_freq_' + target_file
    # concor_save_path = save_path + '/result_conc_' + target_file

    if ".csv" in target_file:
        # dot_arr = target_file.split('.')
        # unbar_arr = dot_arr[0].split('_')
        # ymd_date = unbar_arr[1][0:8]

        # key = ymd_date

        # if files_dictionary.get(key) is None:
        #     files_dictionary[key] = {
                # "path": save_path + '/' + target_file,
                # "morphs": []
            # }

        morphs = []
        txt_arr = pd.read_csv(target_file, encoding="CP949")
        for txt in txt_arr.text:
            txt_morphs = mecab.nouns(txt)
            morphs = morphs + [text for text in txt_morphs if text not in stopwords and len(text) > 1]
            # print(morphs)

            sentence = ''
            for word in txt_morphs:
                if len(word) > 1 and word not in stopwords:
                    print(word)
                    sentence += word + ' '

            ext_save_path = save_path + "/xx_{}".format("example30.csv")
            if not os.path.isfile(ext_save_path):
                with open(ext_save_path, 'w', encoding="utf-8") as f:
                    f.write("{}\n".format(sentence))
            else:
                with open(ext_save_path, 'a', encoding="utf-8") as f:
                    f.write("{}\n".format(sentence))

        # nouns_counter = Counter(morphs)
        # files_dictionary[key]["morphs"] = morphs
        # files_dictionary[key]["noun_counter"] = nouns_counter

    exit()
    morphs = []
    for key, item in files_dictionary.items():
        morphs = morphs + [text for text in item["morphs"] if text not in stopwords and len(text) > 1]

    nouns_counter = Counter(morphs)
    nouns_dict = dict(nouns_counter.most_common(200))

    df_dct = {}
    for t_key in nouns_dict.keys():
        df_dct[t_key] = []
        for key, item in files_dictionary.items():
            noun_dict = item["noun_counter"]
            df_dct[t_key].append(noun_dict[t_key])

    text_id, id_text = {}, {}
    id = 0
    for noun in nouns_dict:
        text_id[noun] = id
        id_text[id] = noun
        id += 1

    target_dict = {}
    for id in id_text.keys():
        target_dict[id] = [0 for i in range(0, len(nouns_dict.keys()))]

    for key, item in files_dictionary.items():
        for n_key, count in item["noun_counter"].items():
            if nouns_dict.get(n_key) is not None:
                nouns_dict[n_key] += count

    rename_dct = {}
    index = 0
    for text in nouns_dict.keys():
        rename_dct[index] = text
        index += 1

    df = pd.DataFrame({
        "word": nouns_dict.keys(),
        "count": nouns_dict.values()
    })
    df.to_csv(freq_save_path, index=False)

    nouns = list(text_id.keys())

    for key, item in files_dictionary.items():
        noun_counter = item["noun_counter"]
        doc_dict = dict(noun_counter)

        for i in range(0, len(nouns)):
            noun_1 = nouns[i]
            j, k = i + 1, i + 1
            for j in range(k, len(nouns)):
                noun_2 = nouns[j]
                if doc_dict.get(noun_1) is not None and doc_dict.get(noun_2) is not None:
                    noun_1_index, noun_2_index = text_id[noun_1], text_id[noun_2]
                    target_dict[noun_1_index][noun_2_index] += 1

    df = pd.DataFrame(target_dict)

    rename_dct = {}
    index = 0
    for text in text_id.keys():
        rename_dct[index] = text
        index += 1
    df.rename(columns=rename_dct, index=rename_dct, inplace=True)

    ndf = df.to_numpy()
    len(ndf)
    for i in range(0, len(ndf)):
        for j in range(0, len(ndf)):
            ndf[i][j] = ndf[j][i]

    df = pd.DataFrame(ndf)
    df.rename(columns=rename_dct, index=rename_dct, inplace=True)
    df.to_csv(concor_save_path)


def preprocess_all(work):
    work = {
        "csv_save_dir": "C:/Users/JHKim/data/csv/3968",
        "proj_directory": "D:/__programming/wctt",
        "work_group_no": 3968,
        "create_tf_idf_table": True,
        "create_tf_table": True,
        "create_tf_coo_table": True,
        "create_wordcloud": True,
    }

    mecab = Mecab()
    save_path = work["csv_save_dir"]
    f = open("./stopwords.txt", 'r', encoding="utf-8")
    stopwords = f.read().split('\n')[0:-2]
    f.close()

    xx_tf_table_save_path = save_path + '/xx_tf_table.csv'
    xx_tf_coo_matrix_save_path = save_path + '/xx_tf_coo_matrix.csv'
    xx_tf_idf_table_save_path = save_path + '/xx_tf_idf_table.csv'
    xx_wc_save_dir = '{}/client/public/wordcloud/{}'.format(work["proj_directory"], work["work_group_no"])
    if not os.path.isdir(xx_wc_save_dir):
        os.makedirs(xx_wc_save_dir, exist_ok=True)

    wc_save_path = xx_wc_save_dir + '/wordcloud.png'
    files = os.listdir(save_path + '/origin')
    files_dictionary = {}

    for file in files:
        if ".csv" in file and (not file.startswith("xx_", 0, 3)):
            dot_arr = file.split('.')
            # unbar_arr = dot_arr[0].split('_')
            # channel = unbar_arr[0]
            # wgid = unbar_arr[1]
            # ymd_date = unbar_arr[2][0:8]
            # key = ymd_date
            key = dot_arr[0]
            # print(key)

            if files_dictionary.get(key) is None:
                files_dictionary[key] = {
                    "path": save_path + '/origin/' + file,
                    "morphs": []
                }

            morphs = []
            files_dictionary[key]["morphs_by_docs"] = []
            files_dictionary[key]["tf_by_docs"] = []
            txt_arr = pd.read_csv(save_path + '/origin/' + file, encoding="CP949")
            for txt in txt_arr.text:
                txt_morphs = mecab.nouns(txt)
                noun_counter_by_docs = Counter(txt_morphs)

                sentence = ''
                for word in txt_morphs:
                    if len(word) > 1:
                        sentence += word + ' '

                ext_save_path = save_path + "/origin/xx_{}".format(file)
                if not os.path.isfile(ext_save_path):
                    with open(ext_save_path, 'w', encoding="utf-8") as f:
                        f.write("{}\n".format(sentence))
                else:
                    with open(ext_save_path, 'a', encoding="utf-8") as f:
                        f.write("{}\n".format(sentence))

                files_dictionary[key]["morphs_by_docs"].append(txt_morphs)
                files_dictionary[key]["tf_by_docs"].append(noun_counter_by_docs)

                morphs = morphs + [text for text in txt_morphs if text not in stopwords and len(text) > 1]

            nouns_counter = Counter(morphs)
            files_dictionary[key]["morphs"] = morphs
            files_dictionary[key]["noun_counter"] = nouns_counter

    morphs = []
    for key, item in files_dictionary.items():
        morphs = morphs + [text for text in item["morphs"] if text not in stopwords and len(text) > 1]

    # exit()

    # print(morphs)
    # model = word2vec.Word2Vec(sentences=morphs, vector_size=100, window=5, min_count=5, workers=4, sg=0)
    # print(model.wv.most_similar("코로나"))
    # exit()

    nouns_counter = Counter(morphs)
    top_nouns = dict(nouns_counter.most_common(200))
    nouns_dict = top_nouns

    text_id, id_text = {}, {}
    id = 0
    for noun in nouns_dict:
        text_id[noun] = id
        id_text[id] = noun
        id += 1

    target_dict = {}
    for id in id_text.keys():
        target_dict[id] = [0 for i in range(0, len(nouns_dict.keys()))]

    for key, item in files_dictionary.items():
        for n_key, count in item["noun_counter"].items():
            if nouns_dict.get(n_key) is not None:
                nouns_dict[n_key] += count


    if work["create_tf_table"]:
        rename_dct = {}
        index = 0
        for text in nouns_dict.keys():
            rename_dct[index] = text
            index += 1

        df = pd.DataFrame({
            "word": nouns_dict.keys(),
            "count": nouns_dict.values()
        })
        df.to_csv(xx_tf_table_save_path, index=False)
        print("Saved: {}".format(xx_tf_table_save_path))

    if work["create_wordcloud"]:
        wordcloud = WordCloud(
            font_path="fonts/NanumGothic.ttf",
            width=800,
            height=800,
            background_color='white',
            max_font_size=200
        )
        wordcloud.generate_from_frequencies(top_nouns)
        plt.figure(figsize=(8, 8))  # 이미지 사이즈 지정
        plt.imshow(wordcloud, interpolation='lanczos')  # 이미지의 부드럽기 정도
        plt.axis('off')  # x y 축 숫자 제거
        plt.savefig(wc_save_path)
        print("Saved: {}".format(wc_save_path))

    nouns = list(text_id.keys())

    for key, item in files_dictionary.items():
        noun_counter = item["noun_counter"]
        doc_dict = dict(noun_counter)

        for i in range(0, len(nouns)):
            noun_1 = nouns[i]
            j, k = i + 1, i + 1
            for j in range(k, len(nouns)):
                noun_2 = nouns[j]
                if doc_dict.get(noun_1) is not None and doc_dict.get(noun_2) is not None:
                    noun_1_index, noun_2_index = text_id[noun_1], text_id[noun_2]
                    target_dict[noun_1_index][noun_2_index] += 1

    if work["create_tf_coo_table"]:
        df = pd.DataFrame(target_dict)

        rename_dct = {}
        index = 0
        for text in text_id.keys():
            rename_dct[index] = text
            index += 1
        df.rename(columns=rename_dct, index=rename_dct, inplace=True)

        ndf = df.to_numpy()
        len(ndf)
        for i in range(0, len(ndf)):
            for j in range(0, len(ndf)):
                ndf[i][j] = ndf[j][i]

        df = pd.DataFrame(ndf)
        df.rename(columns=rename_dct, index=rename_dct, inplace=True)
        df.to_csv(xx_tf_coo_matrix_save_path)
        print("Saved: {}".format(xx_tf_coo_matrix_save_path))

    if work["create_tf_idf_table"]:
        df_dict = {}
        docs_count = 0 #len(files_dictionary.keys())
        for noun in top_nouns.keys():
            df_dict[noun] = 0
            for key, item in files_dictionary.items():
                for doc in item["morphs_by_docs"]:
                    docs_count += 1
                    if noun in doc:
                        df_dict[noun] += 1
                        continue
        print("docs_count: {}".format(docs_count))
        for _, item in files_dictionary.items():
            item["tfidf_by_docs"] = []
            for doc_tf in item["tf_by_docs"]:
                doc_tfidf = []
                for df_key, df_value in df_dict.items():
                    tf = 0 if doc_tf.get(df_key) is None else doc_tf[df_key]
                    idf = log(docs_count / (1 + df_value))
                    doc_tfidf.append(tf * idf)
                item["tfidf_by_docs"].append(doc_tfidf)

        zhp = ZHPandas()
        doc_index = 1
        tfidf_df = pd.DataFrame()
        for _, item in files_dictionary.items():
            for doc_tfidf in item["tfidf_by_docs"]:
                doc_id = "doc" + str(doc_index)
                df = zhp.create_data_frame_to_dict({doc_id: doc_tfidf})
                tfidf_df = zhp.concat_column(tfidf_df, df)
                doc_index += 1

        rename_dct = {}
        index = 0
        for text in df_dict.keys():
            rename_dct[index] = text
            index += 1
        tfidf_df.rename(index=rename_dct, inplace=True)
        tfidf_df.to_csv(xx_tf_idf_table_save_path)
        print("Saved: {}".format(xx_tf_idf_table_save_path))

# preprocess_all({})

# preprocess_one({})