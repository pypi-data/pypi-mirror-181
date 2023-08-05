""" wenxin global variables """
import os
from wenxin_api.const import SOURCE_WENXIN, SOURCE_CONSOLE
# http request
TIMEOUT_SECS = 600
MAX_CONNECTION_RETRIES = 2
REQUEST_SLEEP_TIME = 20
ACCESS_TOKEN_URL = "https://wenxin.baidu.com/moduleApi/portal/api/oauth/token"
ACCESS_TOKEN_URL_CONSOLE = "https://aip.baidubce.com/oauth/2.0/token"

API_REQUEST_URLS = ["https://wenxin.baidu.com/moduleApi/portal/api/rest/1.0/ernie/3.0.20/zeus", # 0
                    "https://wenxin.baidu.com/moduleApi/portal/api/rest/1.0/ernie/3.0.21/zeus", # 1
                    "https://wenxin.baidu.com/moduleApi/portal/api/rest/1.0/ernie/3.0.22/zeus", # 2
                    "https://wenxin.baidu.com/moduleApi/portal/api/rest/1.0/ernie/3.0.23/zeus", # 3
                    "https://wenxin.baidu.com/moduleApi/portal/api/rest/1.0/ernie/3.0.24/zeus", # 4
                    "https://wenxin.baidu.com/moduleApi/portal/api/rest/1.0/ernie/3.0.25/zeus", # 5 
                    "https://wenxin.baidu.com/moduleApi/portal/api/rest/1.0/ernie/3.0.26/zeus", # 6
                    "https://wenxin.baidu.com/moduleApi/portal/api/rest/1.0/ernie/3.0.27/zeus", # 7
                    "https://wenxin.baidu.com/moduleApi/portal/api/rest/1.0/ernie/3.0.28/zeus", # 8
                    "https://wenxin.baidu.com/moduleApi/portal/api/rest/1.0/ernie/3.0.30/zeus", # 9
                    "https://wenxin.baidu.com/moduleApi/portal/api/rest/1.0/ernie/1.0/tuning-train", # 10
                    "https://wenxin.baidu.com/moduleApi/portal/api/rest/1.0/ernie/1.0/tuning-inference",] # 11

VILG_CREATE_URL = "https://wenxin.baidu.com/moduleApi/portal/api/rest/1.0/ernievilg/v1/txt2img"
VILG_RETRIEVE_URL = "https://wenxin.baidu.com/moduleApi/portal/api/rest/1.0/ernievilg/v1/getImg"

VILG_CREATE_URL_CONSOLE = "https://aip.baidubce.com/rpc/2.0/ernievilg/v1/txt2img"
VILG_RETRIEVE_URL_CONSOLE = "https://aip.baidubce.com/rpc/2.0/ernievilg/v1/getImg"

SOURCE = SOURCE_WENXIN


ak = os.environ.get("WENXINAPI_AK", None)
sk = os.environ.get("WENXINAPI_SK", None)
access_token = os.environ.get("WENXINAPI_ACCESS_TOKEN", None)
debug = False
proxy = None
