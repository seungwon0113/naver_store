import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# google_sheets
GOOGLE_SHEETS_JSON_PATH = os.environ["GOOGLE_SHEETS_JSON_PATH"]
GOOGLE_SHEETS_SPREADSHEET_URL = os.environ["GOOGLE_SHEETS_SPREADSHEET_URL"]

# gemini
GENAI_API_KEY = os.environ["GENAI_API_KEY"]
GENAI_API_MODEL = os.environ["GENAI_API_MODEL"]

# naver_data_lab
NAVER_DATA_SHEETS_NAME = os.environ["NAVER_DATA_SHEETS_NAME"]
NAVER_LIST_1000 = os.environ["NAVER_LIST_1000"]
NAVER_LIST_1000_NUM = os.environ["NAVER_LIST_1000_NUM"]
NAVER_KEYWORD = os.environ["NAVER_KEYWORD"]
NAVER_HREF = os.environ["NAVER_HREF"]
NAVER_DATA_LAB_URL = os.environ["NAVER_DATA_LAB_URL"]

# temu_data_tag
TEMU_DATA_SHEETS_NAME = os.environ["TEMU_DATA_SHEETS_NAME"]
TEMU_TITLE_TAG = os.environ["TEMU_TITLE_TAG"]
TEMU_PRICE_TAG = os.environ["TEMU_PRICE_TAG"]
TEMU_IMAGE_TAG = os.environ["TEMU_IMAGE_TAG"]
TEMU_HREF = os.environ["TEMU_HREF"]
TEMU_BEST_SELLER_URL = os.environ["TEMU_BEST_SELLER_URL"]