import os, gspread, time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

load_dotenv()

json_file_path = os.environ['GOOGLE_SHEETS_JSON_PATH']
gc = gspread.service_account(json_file_path)
spreadsheet_url = os.environ['GOOGLE_SHEETS_SPREADSHEET_URL']
doc = gc.open_by_url(spreadsheet_url)

worksheet = doc.worksheet("시트1")
worksheet.update_acell("A1:A2","자동화 끝!")

# TODO: 세팅 완료 후 주석 풀고 드라이버에 옵션 추가
options = Options()
options.add_argument("--headless")

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

driver.get(os.environ['DATA_URL'])
time.sleep(5)


datetime_elements = driver.find_elements(By.CSS_SELECTOR, ".title_cell .datetime")
period_elements = driver.find_elements(By.CSS_SELECTOR, ".title_cell .period")

date_texts = [dt.text for dt in datetime_elements]
period_texts = [pd.text for pd in period_elements]

print("날짜:", date_texts)
print("기간:", period_texts)

# 키워드/링크 가져오기
rank_list = driver.find_elements(By.CSS_SELECTOR, ".rank_list .list_area")
records = [[item.text.strip(), item.get_attribute("href")] for item in rank_list]

print(rank_list)
print(records)

# 시트에 한 번에 저장 (A2 ~)
worksheet.update(f"A2:B{len(records)+1}", records)
