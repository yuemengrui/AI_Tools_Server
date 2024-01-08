# *_*coding:utf-8 *_*
# @Author : YueMengRui
from pydantic import BaseModel, Field, AnyUrl
from typing import Dict, List, Optional


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


class LayoutRequest(BaseModel):
    image: Optional[str] = Field(default=None,
                                 description="图片base64编码，不包含base64头, 与url二选一，优先级image > url")
    url: Optional[AnyUrl] = Field(default=None, description="图片URL")
    score_threshold: Optional[float] = Field(default=0.5, ge=0, le=1)


class LayoutOne(BaseModel):
    box: List[int]
    label: str
    score: float


class LayoutResponse(BaseModel):
    object: str = "Layout"
    data: List[LayoutOne]
    time_cost: Dict = {}


class Callback(BaseModel):
    url: AnyUrl = Field(
        description='回调地址，接收结果回调，接收json请求，请求参数示例：{"params1":"下面的params参数","params2":"下面的params参数"..., "data":{AI处理的结果}}')
    params: Dict = Field(default={}, description='回调参数')


class PDFLoaderRequest(BaseModel):
    pdf_url: Optional[AnyUrl] = Field(description="PDF URL")
    callback: Callback = Field(description='回调配置')
