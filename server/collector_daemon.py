import os
import time
from multiprocessing import Process, freeze_support, Queue
from datetime import datetime, timedelta
import dbconn
import url_collector_nav as ucnb
import url_collector_twt as uct
import url_collector_ins as uci
import url_collector_dna as ucd
import datetime as pydatetime
import html_downloader as hd
import config as cfg

current_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
conf = cfg.get_config(path=current_path)


def date_range(start, end):
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end - start).days + 1)]
    return dates


def collect_urls(work, q):
    channel = work["channel"]
    general_type = ["nav", "twt", "dna", "jna"]
    if channel in general_type:
        date_list = date_range(work["start_date"], work["end_date"])
        print(date_list)
        for date in date_list:
            work["start_date"] = date
            work["end_date"] = date

            if channel == "nav":
                ucnb.collect_urls(work, q)

            if channel == "twt":
                uct.collect_urls(work)

            if channel == "dna":
                ucd.collect_urls(work, q)

    if channel == "ins":
        uci.collect_urls(work, q)


def collect_html(work, q):
    date_list = date_range(work["start_date"], work["end_date"])
    for date in date_list:
        work["start_date"] = date
        work["end_date"] = date
        hd.download(work, q)


if __name__ == '__main__':

    freeze_support()
    while True:
        # DB 조회
        work_group_list = dbconn.session.query(dbconn.WorkGroups).filter(
            dbconn.WorkGroups.work_state == 'attached').all()
        for wg in work_group_list:
            wg.mq_timestamp = str(int(pydatetime.datetime.now().timestamp()))
            time.sleep(0.5)
        dbconn.session.commit()
        dbconn.session.flush()

        for wg in work_group_list:
            dbconn.session.query(dbconn.WorkGroups) \
                .filter(dbconn.WorkGroups.id == wg.id) \
                .update({dbconn.WorkGroups.work_state: "working"})
            dbconn.session.commit()

            channels = wg.channels.split(',')
            procs = []
            for channel in channels:
                keywords = wg.keywords.split(',')
                for keyword in keywords:
                    work = {
                        "channel": channel,
                        "keyword": keyword,
                        "start_date": str(wg.start_date),
                        "end_date": str(wg.end_date),
                        "work_type": "collect_url",
                        "work_group_no": wg.id,
                        "limit_url_count": conf[channel]["limit_url_count"],
                        "invoke_url_count": conf[channel]["invoke_url_count"],
                        "data_directory": wg.data_directory,
                        "proj_directory": wg.proj_directory
                    }

                    html_save_dir = wg.data_directory + '/html/' + str(wg.id)
                    if not os.path.isdir(html_save_dir):
                        os.makedirs(html_save_dir, exist_ok=True)

                    csv_save_dir = wg.data_directory + '/csv/' + str(wg.id)
                    if not os.path.isdir(csv_save_dir):
                        os.makedirs(csv_save_dir, exist_ok=True)

                    work["html_save_dir"] = html_save_dir
                    work["csv_save_dir"] = csv_save_dir

                    q = Queue()
                    procs.append(Process(target=collect_urls, args=(work, q,)))
                    procs.append(Process(target=collect_html, args=(work, q,)))

            for proc in procs:
                proc.start()

        time.sleep(3)
