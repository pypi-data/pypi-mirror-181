from fastapi import APIRouter, Depends
from api.middleware.oauth import token_is_true
from loguru import logger as log
from common.response import Response

from config.zk_config import get_zk
from py_practice.service import zk_service


router = APIRouter(prefix="/zk", tags=["zookeeper"], dependencies=[Depends(token_is_true)])


@router.get("/")
def read_root():
    log.info("你好,欢迎访问zookeeper服务")
    return Response.success(data=None, message="zookeeper service")


@router.get("/list/", name="check exist")
def router_check_path_exist():
    nodes = zk_service.get_list("/")
    if nodes:
        return Response.success(data=nodes, message="查询子节点成功")
    else:
        return Response.error(code=400, message="子节点为空")
