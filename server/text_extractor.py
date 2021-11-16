import os
import config as cfg
from modules.extractor.ExtractorMiddleNode import ExtractorMiddleNode
from modules.extractor.ExtractorTextNode import ExtractorTextNode
from modules.zhbase.ZHPickle import ZHPickle

current_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
conf = cfg.get_config(path=current_path)
model_path = current_path + "/models/"
channel_spec = conf["channel_spec"]

def create_doc_text_blocks(work):

    channel, keyword, date, source = \
        work["channel"], work["keyword"], work["start_date"], work["source"]

    content_ptp_list = work["model"]["content_ptp_list_path"]
    taf_rank_dict = work["model"]["taf_rank_path"]
    taf_boundary_rank = work["model"]["taf_boundary_rank"]

    str_text_nodes = ''
    try:
        mid_text_nodes = 'text,tp,taf_rank\n'
        wd = ExtractorMiddleNode()
        items = wd.create_text_node_list(source)
        for item in items:
            text = item["text"]
            ptp = item["tp"]
            taf_rank = 1 if taf_rank_dict.get(text) is None else taf_rank_dict.get(text)
            mid_text_nodes += '{},{},{}\n'.format(text, ptp, taf_rank)
            if (ptp in content_ptp_list) and (taf_rank <= taf_boundary_rank)\
                    and len(text) > 2:
                str_text_nodes += '{} '.format(text)

    except Exception as e:
        print(e)

    return str_text_nodes


def extract(work):

    channel, keyword, work_group_no, index, date, source = \
        work["channel"], work["keyword"], work["work_group_no"], work["index"], work["start_date"], work["source"]

    str_text_nodes = ''
    if conf["model"].get(channel) is not None:
        content_ptp_list_path = model_path + channel + '/' + conf["model"][channel]["content_ptp_list"]
        taf_rank_path = model_path + channel + '/' + conf["model"][channel]["taf_rank"]
        taf_boundary_rank = conf["model"][channel]["taf_boundary_rank"]

        zhpk = ZHPickle()
        # models[channel] = {
        #     "content_ptp_list_path": zhpk.load(content_ptp_list_path),
        #     "taf_rank_path": zhpk.load(taf_rank_path),
        #     "taf_boundary_rank": taf_boundary_rank
        # }
        #
        # work["model"] = models[channel]

        content_ptp_list = zhpk.load(content_ptp_list_path) #work["model"]["content_ptp_list_path"]
        taf_rank_dict = zhpk.load(taf_rank_path) #work["model"]["taf_rank_path"]
        taf_boundary_rank = taf_boundary_rank #work["model"]["taf_boundary_rank"]


        try:
            mid_text_nodes = 'text,tp,taf_rank\n'
            wd = ExtractorMiddleNode()
            items = wd.create_text_node_list(source)
            for item in items:
                text = item["text"]
                ptp = item["ptp"]
                taf_rank = 1 if taf_rank_dict.get(text) is None else taf_rank_dict.get(text)
                mid_text_nodes += '{},{},{}\n'.format(text, ptp, taf_rank)
                if (ptp in content_ptp_list) and (taf_rank <= taf_boundary_rank) \
                        and len(text) > 2:
                    str_text_nodes += '{} '.format(text)

        except Exception as e:
            print(e)

    return str_text_nodes


# work = {
#     "channel": "nav",
#     "keyword": "코로나백신",
#     "start_date": "2021-03-19",
#     "end_date": "2021-03-19",
#     "work_group_no": 20,
#     "limit_url_count": conf["nav"]["limit_url_count"],
#     "invoke_url_count": conf["nav"]["invoke_url_count"]
# }

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
