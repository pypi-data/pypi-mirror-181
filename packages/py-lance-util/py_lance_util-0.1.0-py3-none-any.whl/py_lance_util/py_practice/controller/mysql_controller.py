from fastapi import APIRouter, Depends
from api.middleware.oauth import token_is_true
from common.response import Response
from db.connection import get_session
from py_practice.controller.main_controller import check_token
from sqlalchemy.orm import sessionmaker

from py_practice.model.student_model import t1
from py_practice.service import mysql_service

router = APIRouter(prefix="/mysql", tags=["mysql"], dependencies=[Depends(token_is_true)])


@router.get("/batch_insert/", name="批量插入")
def test_mysql(params: dict, db: sessionmaker = Depends(get_session)):
    if not check_token(params.get("token")):
        return Response.error(code=500, message="验证失败")
    num = params.get("num", 10)
    data_list = mysql_service.generate_data(t1, num)
    mysql_service.batch_insert_data(db, data_list)
    db.commit()
    entity = db.query(t1).first()
    return Response.success(data=entity, message=f"插入成功，共插入{num}条")
