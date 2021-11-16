import os

import numpy as np

import config as cfg
import modules.collect.dir as dir
from modules.zhbase.ZHPandas import ZHPandas
from modules.zhbase.ZHPickle import ZHPickle
from konlpy.tag import Hannanum
from konlpy.tag import Okt

from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image

conf = cfg.get_config(path=dir.config_path)
html_save_dir = conf["storage"]["html_save_dir"]
csv_save_dir = conf["storage"]["csv_save_dir"]
model_path = dir.model_path
channel_spec = conf["channel_spec"]


# print(html_save_dir)
# print(csv_save_dir)
# print(model_path)

# (1) tf(d,t) : 특정 문서 d에서의 특정 단어 t의 등장 횟수.
# (2) df(t) : 특정 단어 t가 등장한 문서의 수.
# (3) idf(d, t) : df(t)에 반비례하는 수.

df_dict = {}
tf_dict = {}
reduced_text_dict = {}
doc_total_count = 0
zhp = ZHPandas()
for csv_save_group_dir, _, _ in os.walk(csv_save_dir):
    print(len(os.listdir(csv_save_group_dir)))
    for file in os.listdir(csv_save_group_dir):
        if file[-4:] == ".csv":
            # if doc_total_count == 1000:
            #     break
            doc_total_count += 1
            filepath = csv_save_group_dir + '/' + file
            print("[", doc_total_count, "]", filepath)
            df = zhp.read_csv(filepath)
            text_list = list(df.loc[:, "text"].values)
            tf_dict[filepath] = {}
            tmp_df_dict = {}
            all_text = ''
            for text in text_list:
                all_text += text

            nouns = []
            morph = Okt()

            try:
                nouns = morph.nouns(all_text)
            except Exception as e:
                print(e)

            for noun in nouns:
                if len(noun) > 1:
                    if tf_dict[filepath].get(noun) is None:
                        tf_dict[filepath][noun] = 1
                    else:
                        tf_dict[filepath][noun] += 1

                    if tmp_df_dict.get(noun) is None:
                        tmp_df_dict[noun] = 1
                    else:
                        tmp_df_dict[noun] += 1

            for item in tmp_df_dict.items():
                noun, count = item[0], item[1]
                if count > 0:
                    if df_dict.get(noun) is None:
                        df_dict[noun] = 1
                    else:
                        df_dict[noun] += 1


idf_dict = {}
df_list = sorted(df_dict.items(), key=lambda x: x[1], reverse=False)
for item in df_list:
    noun, df_count = item[0], item[1]
    idf_value = np.log(doc_total_count / (1 + df_count))
    idf_dict[noun] = idf_value
    # print("{}: {:.3f} ({}), ".format(noun, idf_value, df_count, ))

tf_idf_dict = {}
for item1 in tf_dict.items():
    filepath, values = item1[0], item1[1]
    values = sorted(values.items(), key=lambda x: x[1], reverse=False)
    for item2 in values:
        text, tf_count = item2[0], item2[1]
        tf_idf_value = tf_count * idf_dict[text]
        tf_idf_dict[text] = tf_idf_value
        print(text, ':', tf_idf_value)

# values = sorted(tf_idf_dict.items(), key=lambda x: x[1], reverse=True)
# for item in values[0:200]:
#     text, value = item[0], item[1]
#     print(text[0:30], value)

# exit()
#             print("Finished {} ...".format(filepath))
#
zhpk = ZHPickle()
zhpk.save("tf_idf_dct.pickle", tf_idf_dict)

# tf_idf_dict = zhpk.load("tf_idf_dct.pickle")

# all_text = ''
# for item in tf_idf_dict.items():
#     text, count = item[0], int(item[1])
#     all_text += (text + ' ') * count
# print(all_text[0:1000])
#
# all_text = " 밀접 밀접 밀접 접촉 접촉 접촉 발생 발생 발생 발생 발생 " \
#            "발생 발생 발생 선제 선제 선제 하루 하루 꼬박 꼬박 꼬박 꼬박 꼬박 꼬박 꼬박 작은방 작은방 작은방 자가 자가 격리 격리 격리 격리 격리 격리 격리 격리 격리 음성 음성 판정 판정 판정 헤프 헤프 헤프 아침 편의점 편의점 편의점 편의점 편의점 편의점 편의점 삼각김밥 삼각김밥 삼각김밥 대충 대충 근처 근처 먹기 물건 물건 물건 물건 하나로마트 하나로마트 하나로마트 고고 고고 충북 충북 충북 단양군 단양군 단양군 단양읍 단양읍 단양읍 상진 상진 상진 매일 매일 매일 매일 매일 숙소 숙소 마트 마트 마트 마트 마트 마트 접근성 접근성 접근성 바로 고자 고자 고자 신발장 신발장 신발장 화투 화투 화투 쇠고리 쇠고리 쇠고리 뭔가 뭔가 뭔가 뭔가 뭔가 뭔가 뭔가 뭔가 뭔가 뭔가 뭔가 뭔가 뭔가 정감 정감 정감 방영 방영 방영 방문 사진 사진 사진 사람 구성 구성 백신 접종 완료 포함 조금 착석 착석 착석 예약 예약 예약 제로 제로 제로 운영 운영 백숙 백숙 백숙 백숙 백숙 백숙 백숙 백숙 백숙 백숙 고민 고민 고민 고민 고민 고민 고민 고민 이유식 이유식 이유식 이유식 이유식 이유식 이유식 부터 부터 수저 수저 수저 개별 개별 개별 포장 포장 엄지 엄지 엄지 개인 개인 개인 개인 개인 개인 개인 개인 개인"


wc = WordCloud(
    background_color="white",
    font_path="fonts/NanumGothic.ttf",
    max_words=100,
    max_font_size=100)
wc.generate_from_frequencies(tf_idf_dict)
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.show()
plt.savefig("wc.png")

exit()

tr = zhpk.load("text_result.pickle")
sorted_dict_tuple = sorted(tr.items(), key=lambda x: x[1], reverse=False)
for tuple in sorted_dict_tuple[0:1000]:
    print(tuple)

from konlpy.tag import Hannanum
hannanum = Hannanum()



#
# df = zhp.read_csv(filename)
