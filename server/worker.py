import os

import network as net
import config as cfg

if __name__ == '__main__':
    current_path = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")
    conf = cfg.get_config(path=current_path)
    net.start_rpc_server(conf["server"]["worker"]["addr"], conf["server"]["worker"]["port"])


