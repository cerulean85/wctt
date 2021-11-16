import os
import config as cfg
from modules.extractor.ExtractorTextNode import ExtractorTextNode
from modules.zhbase.ZHPickle import ZHPickle
from multiprocessing import Process, freeze_support, Queue

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
    html_save_dir = conf["storage"]["html_save_dir"] + str(work_group_no) + '/' + channel
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

if __name__ == "__main__":
    freeze_support()
    work = {
        "channel": "ins",
        "keyword": "코로나백신",
        "start_date": "2021-02-26",
        "end_date": "2021-02-26",
        "work_group_no": 19,
        "limit_url_count": conf["nav"]["limit_url_count"],
        "invoke_url_count": conf["nav"]["invoke_url_count"]
    }

    date_list1 = ["2021-02-26"]
    procs = []
    procs.append(Process(target=iter_extract, args=(work, date_list1,)))
    for p in procs:
        p.start()