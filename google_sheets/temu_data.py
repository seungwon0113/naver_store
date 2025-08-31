import os
import gspread
from dotenv import load_dotenv
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

load_dotenv()

json_file_path = os.environ['GOOGLE_SHEETS_JSON_PATH']
gc = gspread.service_account(json_file_path)
spreadsheet_url = os.environ['GOOGLE_SHEETS_SPREADSHEET_URL']
doc = gc.open_by_url(spreadsheet_url)

worksheet = doc.worksheet(os.environ['TEMU_DATA_SHEETS_NAME'])

# 드라이버 옵션
options = Options()
options.add_argument("--headless")

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

driver.get(os.environ['TEMU_BEST_SELLER_URL'])

worksheet.update(range_name="A2", values=[["시트 자동화 테스트",]])