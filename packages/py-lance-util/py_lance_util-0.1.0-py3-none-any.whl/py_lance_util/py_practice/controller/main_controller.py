from fastapi import APIRouter, Depends
from api.middleware.oauth import token_is_true
from loguru import logger as log
from common.response import Response

from config.config import get_settings
from db.connection import get_session
from py_practice.model.student_model import student, t1
from py_practice.service import main_service

router = APIRouter(prefix="/main", tags=["main"], dependencies=[Depends(token_is_true)])

setting = get_settings()


@router.get("/")
def read_root():
    log.info("你好,欢迎访问main服务")
    return {"code": "200", "success":True, "msg":"main service"}


def check_token(param_token):
    token = setting.token
    return token == param_token
        