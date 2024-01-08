# *_*coding:utf-8 *_*
# @Author : YueMengRui
import os

FASTAPI_TITLE = 'AI_Tools_Servers'
FASTAPI_HOST = '0.0.0.0'
FASTAPI_PORT = 24614

LOG_DIR = 'logs'
os.makedirs(LOG_DIR, exist_ok=True)
TEMP = './temp'
os.makedirs(TEMP, exist_ok=True)

API_OCR_GENERAL = 'http://paimongpt_ocr_center:24666/ai/ocr/general'

LAYOUT_MODEL_PATH = '/workspace/Models/layout_m_960.pt'
LAYOUT_LABELS = ['directory', 'header', 'footer', 'title', 'text', 'table_caption', 'table', 'figure_caption', 'figure',
                 'seal']

# API LIMIT
API_LIMIT = {
    "base": "60/minute",
    "layout": "600/minute"
}
