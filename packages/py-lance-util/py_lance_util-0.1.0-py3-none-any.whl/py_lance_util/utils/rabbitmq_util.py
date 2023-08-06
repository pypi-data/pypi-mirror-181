import threading
from typing import Callable
from loguru import logger
import pika


class RabbitMQ:
    """Rabbitmq工具类"""
    connection = None
    channel = None

    def __init__(self, host, vhost, username, password, port=5672):
        try:
            credential = pika.PlainCredentials(username, password)
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host, port, vhost, credential, heartbeat=0))
            self.channel = self.connection.channel()
        except Exception as e:
            print("rabbitmq init error, please check the config")

    def close(self):
        """关闭连接"""
        if self.connection:
            self.connection.close()
        else:
            print("connection already disconnected")

    def bind_queue_exchange(self, queue, exchange, routing_key):
        """绑定queue和exchange"""
        self.channel.queue_bind(exchange=exchange, queue=queue, routing_key=routing_key)

    def new_queue(self, queue):
        """声明queue，如不存在，则创建"""
        self.channel.queue_declare(queue=queue, durable=True, arguments={'x-message-ttl': 259200000})

    def del_queue(self, queue):
        """Delete the queue"""
        self.channel.queue_delete(queue)

    def new_exchange(self, exchange):
        """声明exchange，如不存在，则创建"""
        self.channel.exchange_declare(exchange=exchange, durable=True, exchange_type='topic')

    def del_exchange(self, exchange):
        """Delete the exchange"""
        self.channel.exchange_delete(exchange=exchange)

    def callback(self, body):
        """接收处理消息的回调函数"""
        super()
        print(str(body).replace('b', '').replace('\'', ''))

    def public_msg(self, exchange, routing_key, json):
        """发布消息"""
        logger.info(f"send:{json}")
        self.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=json)

    def receive_message(self, queue: str, callback):
        # Receive a message
        self.channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

    def stop_consuming(self):
        self.channel.stop_consuming()

    def start_consuming_thread(self, queue: str, callback: Callable):
        # Start a new thread to consume messages
        thread = threading.Thread(target=self.receive_message, args=(queue, callback))
        thread.start()

    def consume_message_with_check(self, queue):
        # 声明一个队列
        self.channel.queue_declare(queue=queue)
        # 消费消息
        method_frame, _, body = self.channel.basic_get(queue=queue, no_ack=True)

        if method_frame:
            # 如果有消息，那么执行消费消息的相关操作
            print('Received message:')
            print(body)
            self.channel.basic_ack(method_frame.delivery_tag)
            # 停止消费消息
            self.channel.basic_cancel(method_frame.consumer_tag)
        else:
            print('No message')
