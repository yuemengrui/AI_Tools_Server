# *_*coding:utf-8 *_*
# @Author : YueMengRui
import time
from mylogger import logger
from fastapi import APIRouter, Request
from info import limiter, layout_model
from configs import API_LIMIT, LAYOUT_LABELS
from .protocol import ErrorResponse, LayoutRequest, LayoutResponse, LayoutOne
from fastapi.responses import JSONResponse
from info.utils.response_code import RET, error_map
from info.utils.common import request_to_image

router = APIRouter()


@router.api_route('/ai/layout/analysis', methods=['POST'], response_model=LayoutResponse, summary="Layout Analysis")
@limiter.limit(API_LIMIT['layout'])
def layout_analysis(request: Request,
                    req: LayoutRequest,
                    ):
    logger.info({'url': req.url, 'score_threshold': req.score_threshold})

    image = request_to_image(req.image, req.url)

    if image is None:
        return JSONResponse(ErrorResponse(errcode=RET.PARAMERR, errmsg=error_map[RET.PARAMERR]).dict(), status_code=500)

    start = time.time()
    try:
        layouts = layout_model.predict(image)
        res = []
        for r in layouts:
            pred = r.boxes.cpu().numpy()
            for i in range(len(pred.cls)):
                if pred.conf[i] > req.score_threshold:
                    res.append(
                        {'box': list(map(int, pred.xyxy[i].tolist())), 'label': LAYOUT_LABELS[int(pred.cls[i])],
                         'score': pred.conf[i]})

        res.sort(key=lambda x: (x['box'][1], x['box'][0]))
        return JSONResponse(LayoutResponse(data=[LayoutOne(**x) for x in res],
                                           time_cost={"layout": f"{time.time() - start:.3f}s"}).dict())
    except Exception as e:
        logger.error({'EXCEPTION': e})
        return JSONResponse(ErrorResponse(errcode=RET.SERVERERR, errmsg=error_map[RET.SERVERERR]).dict(),
                            status_code=500)
