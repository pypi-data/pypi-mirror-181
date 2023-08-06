# 发送邮件
from datetime import datetime

from loguru import logger
from sqlalchemy.orm import sessionmaker
from config.config import get_settings
from py_practice.model.student_model import t1
from utils.rabbitmq_util import RabbitMQ

setting = get_settings()

