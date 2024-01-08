# *_*coding:utf-8 *_*
# @Author : YueMengRui
import os
import time
import requests
from mylogger import logger
from info.background_tasks.document_loader import doc_loader
from fastapi import APIRouter, Request, BackgroundTasks
from info import limiter
from configs import API_LIMIT, TEMP
from .protocol import ErrorResponse, PDFLoaderRequest
from fastapi.responses import JSONResponse
from info.utils.response_code import RET, error_map
from info.utils.pdf_layout_loader import PDFLayoutLoader

router = APIRouter()


@router.api_route('/ai/doc_loader/pdf', methods=['POST'], summary="PDF Loader")
@limiter.limit(API_LIMIT['base'])
def doc_loader_pdf(request: Request,
                   req: PDFLoaderRequest,
                   background_tasks: BackgroundTasks
                   ):
    logger.info(req.dict())

    temp_path = os.path.join(TEMP, str(time.time() * 100000000) + '.pdf')

    try:
        with open(temp_path, 'wb') as f:
            f.write(requests.get(req.pdf_url).content)
    except Exception as e:
        logger.error({'EXCEPTION': e})
        return JSONResponse(ErrorResponse(errcode=RET.PARAMERR, errmsg=error_map[RET.PARAMERR]).dict(), status_code=500)

    background_tasks.add_task(doc_loader, PDFLayoutLoader(), temp_path, req)

    return JSONResponse({'msg': u'成功'})
