import threading
import time

from loguru import logger
from config.config import get_settings

from utils.rabbitmq_util import RabbitMQ
setting = get_settings()


class MyThread(threading.Thread):
    def __init__(self, thread_id, name, counter):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.counter = counter

    def run(self):
        print(f'Starting {self.name}')
        # 这里可以写要执行的任务代码
        rabbitmq_consume()
        print(f'Exiting {self.name}')


def rabbitmq_consume():
    try:
        logger.info("开始消费")
        # Create threads
        rmq = RabbitMQ(
            host=setting.rabbit_mq_host,
            port=setting.rabbit_mq_port,
            vhost=setting.rabbit_mq_vhost,
            username=setting.rabbit_mq_user,
            password=setting.rabbit_mq_psw
        )
        print(rmq)
        # 声明一个队列
        queue = 'queue_hello'
        rmq.receive_message(
            queue=queue,
            callback=message_callback
        )
    except Exception as e:
        logger.error(f"comsumer exception{e}")
    finally:
        rmq.close()


# Define a callback function
def message_callback(channel, method, properties, body):
    time.sleep(1)
    logger.info(f'Received: {body.decode("utf-8")}')


def start_background_job():
    t1 = MyThread(1, "Thread-Comsumer", 1)
    t1.start()
