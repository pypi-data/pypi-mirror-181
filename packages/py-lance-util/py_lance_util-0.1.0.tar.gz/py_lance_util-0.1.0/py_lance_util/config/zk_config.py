from config import config
from kazoo.client import KazooClient

setting = config.get_settings()


def get_zk(ip=setting.ip, port=2181):
    client = KazooClient(hosts=f'{ip}:{port}')
    return client
