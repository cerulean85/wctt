import pandas as pd

class ZHPandas:
    def save_csv(self, df, filename, m_sep=','):
        df.to_csv(filename, sep=m_sep)

    def read_csv(self, filename):
        return pd.read_csv(filename)

    def create_data_frame_to_dict(self, data_dict):
        """
        예시)
            sr_dict = {
                "text": self.__txt_freq_table.keys(),
                "freq": self.__txt_freq_table.values()
            }

        :param data_dict:
        :return:
        """
        df = pd.DataFrame(data=data_dict)
        return df

    def sort_df(self, df, by, ascending=False):
        df = df.sort_values(by=by, ascending=ascending)
        return df

    def group_by_df(self, df, base_df):
        df = df.groupby(base_df)
        return df

    def concat_row(self, df1, df2):
        return pd.concat([df1, df2], ignore_index=True)

    def concat_column(self, df1, df2):
        return pd.concat([df1, df2], axis=1)