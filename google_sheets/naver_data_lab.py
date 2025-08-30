import os
import gspread
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

json_file_path = os.environ['GOOGLE_SHEETS_JSON_PATH']
gc = gspread.service_account(json_file_path)
spreadsheet_url = os.environ['GOOGLE_SHEETS_SPREADSHEET_URL']
doc = gc.open_by_url(spreadsheet_url)

worksheet = doc.worksheet(os.environ['GOOGLE_SHEETS_NAME'])

# 드라이버 옵션
options = Options()
options.add_argument("--headless")

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

driver.get(os.environ['DATA_URL'])

records = []
rank_counter = 1

while True:
    # 현재 페이지의 랭킹 아이템 20개 수집
    rank_items = WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, os.environ["LIST_1000"])
        )
    )

    for li in rank_items:
        num_el = li.find_element(By.CSS_SELECTOR, os.environ["LIST_1000_NUM"])
        rank_num = int(num_el.text.strip())

        keyword_el = li.find_element(By.CSS_SELECTOR, os.environ["KEYWORD"])
        full_text = keyword_el.text.strip()
        keyword = full_text.replace(num_el.text.strip(), "").strip()
        link = keyword_el.get_attribute(os.environ["HREF"])


        records.append([rank_num, keyword, link])

        if rank_num >= 500:
            print("Top 500 수집 완료, 종료합니다.")
            driver.quit()
            worksheet.update(range_name="A2", values=records)
            exit()

    print(f"현재까지 수집된 개수: {len(records)}")

    # 다음 버튼 확인
    try:
        next_btn = driver.find_element(By.CSS_SELECTOR, "a.btn_page_next")

        if "disabled" in next_btn.get_attribute("class"):
            break  # 마지막 페이지 → 종료

        driver.execute_script("arguments[0].click();", next_btn)
        time.sleep(1)

    except Exception as e:
        print("error:", e)
        break
