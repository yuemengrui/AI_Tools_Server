# *_*coding:utf-8 *_*
# @Author : YueMengRui
import os
import cv2
import uuid
import shutil
import requests
import datetime
from mylogger import logger
from fastapi import APIRouter, Request
from info import limiter
from configs import TEMP, API_LIMIT
from .protocol import TableRequest, ErrorResponse, TableResponse, TableCell, TableImage
from fastapi.responses import JSONResponse
from info.utils.response_code import RET, error_map
from info.utils.box_segmentation import get_box
from info.utils.ocr import get_ocr_byte_res
from info.utils.image_draw import draw_image
from info.utils.file_upload import upload_file

router = APIRouter()


@router.api_route('/ai/table/ocr', methods=['POST'], response_model=TableResponse, summary="Table OCR")
@limiter.limit(API_LIMIT['base'])
def table_ocr(request: Request,
              req: TableRequest,
              ):
    try:
        file_data = requests.get(req.file_url).content
    except Exception as e:
        logger.error(e)
        return JSONResponse(ErrorResponse(errcode=RET.PARAMERR, errmsg=error_map[RET.PARAMERR]).dict(), status_code=500)

    nowtime = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    img_path = os.path.join(TEMP, str(nowtime) + '-' + uuid.uuid1().hex + '.jpg')

    try:
        with open(img_path, 'wb') as f:
            f.write(file_data)
    except Exception as e:
        logger.error(e)
        return JSONResponse(ErrorResponse(errcode=RET.IOERR, errmsg=error_map[RET.IOERR]).dict(), status_code=500)

    origin_img = cv2.imread(img_path)

    if origin_img is None:
        return JSONResponse(ErrorResponse(errcode=RET.IOERR, errmsg=error_map[RET.IOERR]).dict(), status_code=500)

    img, boxes = get_box(origin_img, **req.table_seg_configs)
    img_h, img_w = img.shape[:2]
    image_protocol = TableImage(height=img_h, width=img_w, origin_url=req.file_url)

    table = []
    for box in boxes:
        crop_img = img[box[1]:box[3], box[0]:box[2]]
        ocr_res = get_ocr_byte_res(crop_img)
        table.append(TableCell(box=box, text=ocr_res))

    if req.redraw:
        canvas = draw_image(img_h, img_w, table)
        canvas.save(img_path)
        try:
            file_url = upload_file(img_path)
            image_protocol.redraw_url = file_url
        except Exception as e:
            logger.error({'EXCEPTION': e})

    shutil.rmtree(img_path, ignore_errors=True)

    return JSONResponse(TableResponse(ocr_results=table, image=image_protocol).dict())
