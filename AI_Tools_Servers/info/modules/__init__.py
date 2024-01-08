# *_*coding:utf-8 *_*
from fastapi import FastAPI
from . import layout, doc_loader


def register_router(app: FastAPI):
    app.include_router(router=layout.router, prefix="", tags=["Layout"])
    app.include_router(router=doc_loader.router, prefix="", tags=["Doc Loader"])
