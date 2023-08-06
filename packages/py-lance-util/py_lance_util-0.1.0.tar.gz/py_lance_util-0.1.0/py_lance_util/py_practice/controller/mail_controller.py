
from fastapi import APIRouter, Depends
from loguru import logger as log
from api.middleware.oauth import token_is_true
from common.response import Response
from py_practice.controller.main_controller import check_token
from py_practice.service import mail_service


router = APIRouter(prefix="/mail", tags=["mail"], dependencies=[Depends(token_is_true)])


@router.post("/send/", name="发送邮件")
def router_send_email(params: dict):
    if not check_token(params.get("token")):
        return Response.error(code=500, message="验证失败，无法发送邮件")
    log.info(f"send email")
    receivers = params.get("receivers")
    if receivers is None or len(receivers) == 0:
        return Response.error(code=500, message="接收方邮件不能为空")
    title = params.get("title", "default title")
    content = params.get("content", "default content")

    result = mail_service.send_email(title, content, receivers)

    if result == 'success':
        return Response.success(message="send successful")
    else:
        return Response.error(message="send fail", code=500)
