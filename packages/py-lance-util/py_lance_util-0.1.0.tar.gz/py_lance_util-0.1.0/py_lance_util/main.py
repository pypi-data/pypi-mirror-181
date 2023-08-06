from loguru import logger as log
import uvicorn
from fastapi import FastAPI
from api import router
from config import config, logger, swagger
from db import connection
from py_practice.background.background import start_background_job


app = FastAPI()


def get_reload():
    import os
    RELOAD = os.getenv("RELOAD", default="true")
    if RELOAD.lower() == "false":
        RELOAD = False
    else:
        RELOAD = True
    return RELOAD


@app.on_event("startup")
def init_whole_system():
    # 初始化profile, 必须放在最前面
    config_setting = config.get_settings()
    log.info(config_setting)
    # 初始化log
    logger.init()

    # 初始化router
    router.init(app, config_setting)

    # router初始化之后 导出 swagger api.json
    config.export_openapi_docs(app.openapi())

    # 初始化数据库链接
    connection.init_connection()

    # init swagger docs
    swagger.init()

    # init data_source
    # data_source.init()

    # start background job
    # start_background_job()


if __name__ == "__main__":
    # 启动
    # RELOAD = get_reload()

    uvicorn.run("main:app", host="0.0.0.0", port=8004, reload=True)
