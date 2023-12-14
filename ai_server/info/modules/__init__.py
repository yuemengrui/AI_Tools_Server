# *_*coding:utf-8 *_*
from fastapi import FastAPI
from . import layout


def register_router(app: FastAPI):
    app.include_router(router=layout.router, prefix="", tags=["Layout"])
