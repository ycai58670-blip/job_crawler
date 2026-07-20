import os

API_URL = "https://api-c.liepin.com/api/com.liepin.searchfront4c.pc-search-job"
KEYWORD = "python开发"
CITY_CODE = "410"
PAGE_SIZE = 40
MAX_PAGES = 20
MAX_RETRY = 3
MIN_SLEEP = 1.5
MAX_SLEEP = 3.0
REQUEST_TIMEOUT = (10, 30)
OUTPUT_FILE = r"D:\Agent\job_crawler\猎聘职位数据.xlsx"

XSRF_TOKEN = os.getenv("LIEPIN_XSRF_TOKEN", "")
INITIAL_SK_ID = os.getenv("LIEPIN_SK_ID", "")
INITIAL_FK_ID = os.getenv("LIEPIN_FK_ID", "")
INITIAL_CK_ID = os.getenv("LIEPIN_CK_ID", "")
COOKIE = os.getenv("LIEPIN_COOKIE", "")

OUTPUT_COLUMNS = [
    "职位ID",
    "职位名称",
    "地点",
    "薪资",
    "学历",
    "更新时间",
    "职位链接",
    "公司名称",
    "公司规模",
    "公司行业",
    "融资阶段",
    "招聘人",
]
