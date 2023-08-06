from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger
from sqlalchemy.exc import DatabaseError


def add_exception(app: FastAPI) -> JSONResponse:
    @app.exception_handler(HTTPException)
    async def http_exception(request: Request, exception: HTTPException):
        import traceback
        err = traceback.format_exc()
        logger.error(err)
        return JSONResponse(
            content={
                "message": exception.detail,
                "code": exception.status_code,
                "success": False,
                "data": None
            },
            status_code=exception.status_code)

    @app.exception_handler(DatabaseError)
    async def database_exception(request: Request, exception: DatabaseError):
        message_str = ("----SQL----: {sql},  ----Error----: {error}").format(
            sql=exception.statement, error=exception.args[0])
        logger.error(message_str)
        return JSONResponse(
            content={
                "message": message_str,
                "code": 500,
                "success": False,
                "data": None
            },
            status_code=500)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        logger.error({"detail": exc.errors(), "body": exc.body})
        return JSONResponse(
            content={
                "message": "输入数据格式有误，请检查",
                "code": 422,
                "success": False,
                "data": {"detail": exc.errors(), "body": exc.body}
            },
            status_code=422)
