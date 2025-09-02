import gspread
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from envs import environments as env
from database import Databases

db = Databases()

gc = gspread.service_account(env.GOOGLE_SHEETS_JSON_PATH)
doc = gc.open_by_url(env.GOOGLE_SHEETS_SPREADSHEET_URL)

worksheet = doc.worksheet(env.NAVER_DATA_SHEETS_NAME)

# 드라이버 옵션
options = Options()
options.add_argument("--headless")

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

driver.get(env.NAVER_DATA_LAB_URL)
time.sleep(5)

# 카테고리별 data-cid 값 (추가 가능)
CATEGORIES = {
    "패션의류": "50000000",
    "생활/건강": "50000008",
}

def scrape_category(driver, worksheet, category_name, data_cid, start_cell):
    print(f"[{category_name}] 스크래핑 시작")

    # 1) 분야 드롭다운 열기
    dropdown_toggle = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "span.select_btn"))
    )
    driver.execute_script("arguments[0].click();", dropdown_toggle)
    time.sleep(1)

    # 2) 카테고리 항목 클릭
    category_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, f"ul.select_list li a.option[data-cid='{data_cid}']")
        )
    )
    driver.execute_script("arguments[0].click();", category_option)
    time.sleep(1)

    # 3) 조회하기 버튼 클릭
    submit_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn_submit"))
    )
    driver.execute_script("arguments[0].click();", submit_btn)
    time.sleep(2)

    # 4) 데이터 수집 시작
    records = []
    while True:
        rank_items = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, env.NAVER_LIST_1000))
        )

        for li in rank_items:
            num_el = li.find_element(By.CSS_SELECTOR, env.NAVER_LIST_1000_NUM)
            rank_num = int(num_el.text.strip())

            keyword_el = li.find_element(By.CSS_SELECTOR, env.NAVER_KEYWORD)
            full_text = keyword_el.text.strip()
            keyword = full_text.replace(num_el.text.strip(), "").strip()
            link = keyword_el.get_attribute(env.NAVER_HREF)

            records.append([rank_num, keyword, link])

            # TODO: 중복 업데이트 처리 필요 (수정예정)
            if category_name == "패션의류":
                db.execute(
                    "INSERT INTO naver_fashion (rank, keyword, link) VALUES (%s, %s, %s) ON CONFLICT (keyword) DO UPDATE SET rank = EXCLUDED.rank, link = EXCLUDED.link",
                    (rank_num, keyword, link),
                    fetch=False,
                )
            elif category_name == "생활/건강":
                db.execute(
                    "INSERT INTO naver_health (rank, keyword, link) VALUES (%s, %s, %s) ON CONFLICT (keyword) DO UPDATE SET rank = EXCLUDED.rank, link = EXCLUDED.link",
                    (rank_num, keyword, link),
                    fetch=False,
                )

            if rank_num >= 500:
                print(f"[{category_name}] Top 500 완료")
                worksheet.update(range_name=start_cell, values=records)
                return

        try:
            next_btn = driver.find_element(By.CSS_SELECTOR, "a.btn_page_next")
            if "disabled" in next_btn.get_attribute("class"):
                break
            driver.execute_script("arguments[0].click();", next_btn)
            time.sleep(1)
        except Exception:
            break

    worksheet.update(range_name=start_cell, values=records)

# 패션의류 → A3부터 저장
scrape_category(driver, worksheet, "패션의류", CATEGORIES["패션의류"], "A3")

# 생활/건강 → D3부터 저장
scrape_category(driver, worksheet, "생활/건강", CATEGORIES["생활/건강"], "D3")
db.close()
driver.quit()