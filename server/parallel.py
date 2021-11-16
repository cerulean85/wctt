import time

import psutil as psutil


class WorkProc:

    def __init__(self, spec, proc):
        self.spec = spec
        self.process = proc


proc_list = []


def add_proc(spec, proc):
    global proc_list
    work_proc = WorkProc(spec, proc)
    proc_list.append(work_proc)


def start_procs(work_type):
    global proc_list

    for proc in proc_list:
        if proc.spec["work_type"] == work_type:
            proc.process.start()

def stop_procs(work):
    global proc_list

    removed_proc_index = []
    for proc_index in range(len(proc_list)):
        proc = proc_list[proc_index]
        if proc.spec["work_group_no"] == work["work_group_no"] and proc.spec["work_no"] == work["work_no"]:

            if proc.process.is_alive():
                proc.process.terminate()
                proc.process.join()
                proc.process.close()
                del proc.process

            removed_proc_index.append(proc_index)

    tmp_proc_list = []
    for proc_index in range(len(proc_list)):
        if not proc_index in removed_proc_index:
            tmp_proc_list.append(proc_list[proc_index])

    proc_list = tmp_proc_list
    print("Current Processing Processes Count: {}".format(len(proc_list)))

#
# def stop_procs(self, pid):
#     time.sleep(3)
#     try:
#         parent_pid = pid
#         parent = psutil.Process(parent_pid)
#         for child in parent.children(recursive=True):
#             child.kill()
#         parent.kill()
#     except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#         pass
