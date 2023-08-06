
from api.middleware.global_exception import add_exception
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from py_practice.controller import mail_controller, main_controller, mq_controller, mysql_controller, zk_controller


def init(app: FastAPI, config_setting):
    add_cros(app)
    add_static_router(app, config_setting)
    add_router(app)
    add_exception(app)


def add_static_router(app, config_setting):
    app.mount("/doc", StaticFiles(directory="doc"), name="doc")
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.mount("/logs", StaticFiles(directory=config_setting.static_log_root), name="logs")


def add_cros(app: FastAPI):
    ### CROS 跨域问题 ###
    app.add_middleware(
        CORSMiddleware,
        allow_origins='*',
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def add_router(app: FastAPI):
    app.include_router(main_controller.router)
    app.include_router(zk_controller.router)
    app.include_router(mq_controller.router)
    app.include_router(mail_controller.router)
    app.include_router(mysql_controller.router)