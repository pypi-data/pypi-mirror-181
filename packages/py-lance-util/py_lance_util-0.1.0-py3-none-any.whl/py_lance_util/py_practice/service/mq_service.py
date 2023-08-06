

from loguru import logger as log
from config.config import get_settings
from utils.rabbitmq_util import RabbitMQ

setting = get_settings()

def rabbitmq_produce(params: dict):
    try:
        # Create the RabbitMQ object
        rmq = RabbitMQ(
            host=setting.rabbit_mq_host,
            port=setting.rabbit_mq_port,
            vhost=setting.rabbit_mq_vhost,
            username=setting.rabbit_mq_user,
            password=setting.rabbit_mq_psw
        )
        exchange = 'exchange_hello'
        queue = 'queue_hello'
        key = 'key_hello'
        rmq.bind_queue_exchange(queue=queue, exchange=exchange, routing_key=key)
        for item in params.get("msg"):
            rmq.public_msg(
                exchange=exchange,
                routing_key=key,
                json=item
            )
    except Exception as e:
        log.error(f"error:{e}")
    finally:
        rmq.close()