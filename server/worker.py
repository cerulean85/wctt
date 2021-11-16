import network as net
import config

if __name__ == '__main__':
    conf = config.get_config()
    net.start_rpc_server(conf["server"]["worker"]["addr"], conf["server"]["worker"]["port"])


