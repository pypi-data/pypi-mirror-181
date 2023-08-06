import os
from loguru import logger


def init():
    log_path = 'logs'
    if not os.path.exists(log_path):
        os.mkdir(log_path)

    log_path_error = os.path.join(log_path, f'demo_error.log')
    log_path_debug = os.path.join(log_path, f'demo_debug.log')
    log_path_info = os.path.join(log_path, f'demo_info.log')

    # 日志记录不在控制台打印
    # logger.remove(handler_id=None)

    logger.add(
        # 输出的文件名
        log_path_error,
        # 日志输出格式
        format="{name} {time:YYYY-MM-DD HH:mm:ss} {level} {message}",
        # 日志级别: DEBUG、INFO、SUCCESS、WARNING、ERROR .....
        level="ERROR",
        # 每隔多久生成一个日志文件 支持按文件大小生成 如 1KB 1MB .....
        rotation='00:00',
        # 是否异步记录
        enqueue=True,
        # 日志文件保存时间
        retention='30 days',
        # 日志文件编码
        encoding='utf-8'
    )

    logger.add(
        log_path_debug,
        format="{name} {time:YYYY-MM-DD HH:mm:ss} {level} {message}",
        level="DEBUG",
        rotation='00:00',
        enqueue=True,
        retention='30 days',
        encoding='utf-8'
    )

    logger.add(
        log_path_info,
        format="{name} {time:YYYY-MM-DD HH:mm:ss} {level} {message}",
        level="INFO",
        rotation='00:00',
        enqueue=True,
        retention='30 days',
        encoding='utf-8'
    )
