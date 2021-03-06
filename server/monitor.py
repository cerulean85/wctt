import json, os, time
import dbconn as db
import config as cfg

def daemon():
    current_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
    conf = cfg.get_config(path=current_path)

    while True:
        work_group_list = db.session.query(db.WorkGroups) \
            .filter(db.WorkGroups.work_state == 'working').all()

        for work_group in work_group_list:
            report = {}
            target_csv_line_count = 0
            html_log_file_path = work_group.data_directory + "/html/" + str(work_group.id) + "/logs.txt"
            csv_save_dir = work_group.data_directory + "/csv/" + str(work_group.id) + '/origin'
            channels = work_group.channels.split(',')
            for channel in channels:
                try:
                    for filename in os.listdir(csv_save_dir):
                        if not filename.startswith(channel, 0, 3):
                            continue

                        target_csv_save_dir = csv_save_dir + '/' + filename
                        file = open(target_csv_save_dir, 'r', encoding="utf-8")
                        # csv_line_count = len(file.readlines()) #file.read().count('\n')+1
                        target_csv_line_count += len(file.readlines())
                        file.close()

                    html_file_count = 0
                    if os.path.isfile(html_log_file_path):
                        html_log_file = open(html_log_file_path, 'r', encoding="UTF8")
                        while True:
                            line = html_log_file.readline()
                            if not line: break
                            print(line)
                            if line.startswith("[{}]".format(channel), 0, 5):
                                html_file_count += 1
                        html_log_file.close()

                    report[channel] = {
                        "html_file_count": html_file_count, #len(os.listdir(target_html_save_dir)),
                        "csv_line_count": target_csv_line_count# len(os.listdir(target_csv_save_dir))
                    }
                    work_group.report = json.dumps(report, ensure_ascii=False)
                    print(report)
                    print(csv_save_dir)
                    print(html_log_file_path)

                    db.session.commit()
                    db.session.flush()
                except Exception as e:
                    print(e)

        time.sleep(3)


    # File Explorer ??????
    # ????????? urls > work_group_no > ????????? url ?????? ???????????? poll????????????.
    # HTML ?????? ?????? > ?????? ?????? > ?????? ??????   len(os.listdir(path))
    # ????????? ?????? ?????? > ?????? ?????? > ?????? ??????    len(os.listdir(path))

    # Kafka URL ??????
    # HTML ?????? ?????? ??????

    # CSV ????????? ????????? ?????? ??????
    # DB ????????????


if __name__ == '__main__':
    # Daemon Start.
    daemon()
    # daemon_obj = Process(target=daemon, args=())
    # daemon_obj.start()

    # conf = config.get_config()
    # net.start_rpc_server(conf["server"]["worker"]["addr"], conf["server"]["worker"]["port"])
