# *_*coding:utf-8 *_*
# @Author : YueMengRui
from pydantic import BaseModel, Field, AnyUrl
from typing import Dict, Literal, List


class ErrorResponse(BaseModel):
    object: str = "error"
    errcode: int
    errmsg: str


class TableRequest(BaseModel):
    file_url: AnyUrl = Field(description="文件URL")
    redraw: bool = Field(default=False, description="是否根据表格内容重新绘制新的图片，默认false")
    table_seg_configs: Dict = Field(default=dict(), description="可选，表格分割超参数")


class TableCell(BaseModel):
    box: List[int]
    text: str


class TableImage(BaseModel):
    height: int
    width: int
    origin_url: str
    redraw_url: str = Field(default=None)


class TableResponse(BaseModel):
    ocr_results: List[TableCell]
    image: TableImage
