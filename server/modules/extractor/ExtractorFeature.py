import pandas as pd
import numpy as np
from modules.zhbase.ZHPandas import ZHPandas

pd.set_option('display.max_columns', None)  ## 모든 열을 출력한다.
pd.set_option('display.max_rows', None)  ## 모든 열을 출력한다.
np.set_printoptions(threshold=np.inf, linewidth=np.inf)


class ExtractorFeature:

    def __init__(self):
        self.__txt_freq_table = {}
        self.__txt_index_table = {}
        self.__tags_freq_table = {}
        self.__tags_index_dict = {}
        self.__freq_count_table = {}
        self.__zhp = ZHPandas()

    def get_context_feature(self, df, is_train=True):
        if is_train:
            # 훈련이 아닌 경우에는 freq 집계할 필요가 없음
            self.__aggregate_freq(df)
            self.__aggregate_text_token()

        basic_feature = self.__get_basic_context_feature(df)
        option_feature = self.__get_tags_pattern_feature(df)

        feature = {
            "x1": option_feature["Tag Path"],
            "x2": basic_feature["Text"],
            "x3": basic_feature["Text Frequency"],
            "x4": basic_feature["Text Index"],
            "x5": option_feature["Current Parent Tag Path Index"],
            "x6": basic_feature["Parent Tag Path Frequency"],
            "x7": option_feature["Prev Parent Tag Path Index 1"],
            "x8": option_feature["Prev Parent Tag Path Index 2"],
            "x9": option_feature["Next Parent Tag Path Index 1"],
            "x10": option_feature["Next Parent Tag Path Index 2"],
            "x11": basic_feature["Text Frequency Group Count"],
            "x12": basic_feature["Parent Tag Path Frequency Group Count"],
            "y": basic_feature["y"],
        }

        return feature

    def __agg_text_freq(self, txt):
        if self.__txt_freq_table.get(txt) is None:
            self.__txt_freq_table[txt] = 1
        else:
            self.__txt_freq_table[txt] += 1

    def __agg_tag_freq(self, txt):
        if self.__tags_freq_table.get(txt) is None:
            self.__tags_freq_table[txt] = 1
        else:
            self.__tags_freq_table[txt] += 1

    def __aggregate_freq(self, df):
        agg_txt_freq = self.__aggregate_text_freq(df)
        agg_tag_freq = self.__aggregate_tags_freq(df)
        return agg_txt_freq, agg_tag_freq

    def __aggregate_text_token(self):
        index = 1
        for txt in self.__txt_freq_table.keys():
            self.__txt_index_table[txt] = index
            index += 1

    def __aggregate_text_freq(self, df):
        txt_list = df.loc[:, ["text"]].values
        for txt_arr in txt_list:
            txt = txt_arr[0]
            self.__agg_text_freq(txt)
            continue

        sr_dict = {
            "text": self.__txt_freq_table.keys(),
            "freq": self.__txt_freq_table.values(), # 동일한 텍스트가 등장한 횟수
        }
        df = self.__zhp.create_data_frame_to_dict(sr_dict)
        df = self.__zhp.sort_df(df, ["freq"])
        return df.reset_index()

    def __aggregate_tags_freq(self, df):
        tags_list = df.loc[:, ["ptp"]].values
        for tags_arr in tags_list:
            tags = tags_arr[0]
            self.__agg_tag_freq(tags)
            continue

        sr_dict = {
            "tags": self.__tags_freq_table.keys(),
            "freq": self.__tags_freq_table.values()
        }
        df = self.__zhp.create_data_frame_to_dict(sr_dict)
        df = self.__zhp.sort_df(df, ["freq"])
        return df.reset_index()

    def __get_tags_pattern_feature(self, df):

        prev_step = 2
        next_step = 2
        prev_tags_pattern_token_1_list = []
        prev_tags_pattern_token_2_list = []
        current_tags_pattern_token_list = []
        next_tags_pattern_token_1_list = []
        next_tags_pattern_token_2_list = []

        tag_list = list(self.__tags_freq_table.keys())
        tag_id_list = {}
        for i in range(0, len(tag_list)):
            tag = tag_list[i]
            tag_id_list[tag] = i + 1

        tags_list = df.loc[:, "ptp"].values.tolist()

        for i in range(0, len(tags_list)):
            if i < prev_step:
                prev_tags_1 = 0
                prev_tags_2 = 0
            else:
                prev_tags_1 = tag_id_list[tags_list[i - prev_step]]
                prev_tags_2 = tag_id_list[tags_list[i - (prev_step + 1)]]

            if i > len(tags_list) - 1 - next_step:
                next_tags_1 = 0
                next_tags_2 = 0
            else:
                next_tags_1 = tag_id_list[tags_list[i + 1]]
                next_tags_2 = tag_id_list[tags_list[i + next_step]]

            prev_tags_pattern_token_1_list.append(prev_tags_1)
            prev_tags_pattern_token_2_list.append(prev_tags_2)
            current_tags_pattern_token_list.append(tag_id_list[tags_list[i]])
            next_tags_pattern_token_1_list.append(next_tags_1)
            next_tags_pattern_token_2_list.append(next_tags_2)

        # print(len(tags_list), len(current_tags_pattern_token_list))
        res_dict = {
            "Tag Path": tags_list,
            "Current Parent Tag Path Index": current_tags_pattern_token_list, # current_tags_pattern_token
            "Prev Parent Tag Path Index 1": prev_tags_pattern_token_1_list, # prev_tags_pattern_token_1
            "Prev Parent Tag Path Index 2": prev_tags_pattern_token_2_list, # prev_tags_pattern_token_2
            "Next Parent Tag Path Index 1": next_tags_pattern_token_1_list, # next_tags_pattern_token_1
            "Next Parent Tag Path Index 2": next_tags_pattern_token_2_list, # next_tags_pattern_token_2
        }

        return res_dict

    def __get_freq_list(self, t_list, txt_freq_table):
        freq_list = []
        # p_freq_list = []
        for i in range(0, len(t_list)):
            txt = t_list[i]
            freq = txt_freq_table[txt]
            freq_list.append(freq)

        return freq_list


    def __get_data_df(self, file_list):
        zhp = ZHPandas()
        df = None
        for filename in file_list:
            if ".csv" not in filename:
                continue

            if df is None:
                df = zhp.read_csv(filename)
            else:
                __df = zhp.read_csv(filename)
                df = pd.concat([df, __df])
        return df

    def __get_text_feature(self, df):
        txt_list = df["text"].values

        # 정수 인코딩
        txt_index_list = []
        for i in range(0, len(txt_list)):
            txt = txt_list[i]
            if self.__txt_index_table.get(txt) is None:
                """
                Out of Text의 경우에는 Index를 새로 추가할 것
                """
                txt_index = len(self.__txt_index_table) # Out of Text
            else:
                txt_index = self.__txt_index_table.get(txt)
            txt_index_list.append(txt_index)

        txt_freq_list = []
        for i in range(0, len(txt_list)):
            txt = txt_list[i]
            if self.__txt_freq_table.get(txt) is None:
                # Out of Text 빈도를 1로 측정
                freq = 1
            else:
                freq = self.__txt_freq_table[txt]
            txt_freq_list.append(freq)

        """
        example:
        - 나는 이번 주에는 운동을 3번 했어요. > freq = 3
        - 나처럼 운동을 3번 한 사람이 10명입니다. > freq_group_count = 10
        """
        txt_freq_group_count_list = []
        for freq in txt_freq_list:
            fg_count = list(self.__txt_freq_table.values()).count(freq)
            txt_freq_group_count_list.append(fg_count)

        return txt_list, txt_index_list, txt_freq_list, txt_freq_group_count_list

    def __get_tags_feature(self, df):
        tags_list = df["ptp"].values
        tags_freq_list = []
        for i in range(0, len(tags_list)):
            tags = tags_list[i]
            if self.__tags_freq_table.get(tags) is None:
                # Out of Tags 빈도를 1로 측정
                freq = 1
            else:
                freq = self.__tags_freq_table[tags]
            tags_freq_list.append(freq)

        """
        example:
        - 나는 이번 주에는 운동을 3번 했어요. > freq = 3
        - 나처럼 운동을 3번 한 사람이 10명입니다. > freq_group_count = 10
        """
        tags_freq_group_count_list = []
        for freq in tags_freq_list:
            fg_count = list(self.__tags_freq_table.values()).count(freq)
            tags_freq_group_count_list.append(fg_count)

        return tags_list, tags_freq_list, tags_freq_group_count_list

    def __get_basic_context_feature(self, df):

        txt_list, txt_token, txt_freq_list, txt_freq_group_count_list = self.__get_text_feature(df)
        tag_list, tag_freq_list, tags_freq_group_count_list = self.__get_tags_feature(df)
        lb_list = df["label"].values

        df_dict = {
            "Text": txt_list, # text
            "Text Index": txt_token, # text_token
            "Text Frequency": txt_freq_list, # text_freq
            "Text Frequency Group Count": txt_freq_group_count_list, # text_freq
            "Parent Tag Path Text": tag_list, # tags
            "Parent Tag Path Frequency": tag_freq_list, # current_tags_freq
            "Parent Tag Path Frequency Group Count": tags_freq_group_count_list, # current_tags_freq
            "y": lb_list #label
        }

        return df_dict
