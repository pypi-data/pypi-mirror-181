
from config.zk_config import get_zk
from loguru import logger as log


def get_list(path):
    try:
        zk = get_zk()
        zk.start()  # 与zookeeper连接
        log.info("connected to zk")
        nodes = zk.get_children(path)
        if nodes:
            return nodes
        else:
            return None
    except Exception as e:
        log.error(f"get node list error error:{e}")
    finally:
        zk.stop()
        log.info("closed zk connection")
