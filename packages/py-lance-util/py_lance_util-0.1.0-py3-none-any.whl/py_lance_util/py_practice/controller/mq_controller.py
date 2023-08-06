from fastapi import APIRouter, Depends
from api.middleware.oauth import token_is_true
from loguru import logger as log
from common.response import Response

from py_practice.controller.main_controller import check_token
from py_practice.service import mq_service


router = APIRouter(prefix="/mq", tags=["mq"], dependencies=[Depends(token_is_true)])


@router.get("/produce/", name="rabbitmq")
def test_connect_rabbitmq(params: dict):
    if not check_token(params.get("token")):
        return Response.error(message="验证失败", code=500)
    mq_service.rabbitmq_produce(params)
    return Response.success(data=params.get("msg"))
