import time

import gspread
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from envs import environments as envs

json_file_path = envs.GOOGLE_SHEETS_JSON_PATH
gc = gspread.service_account(json_file_path)
spreadsheet_url = envs.GOOGLE_SHEETS_SPREADSHEET_URL
doc = gc.open_by_url(spreadsheet_url)

worksheet = doc.worksheet(envs.TEMU_DATA_SHEETS_NAME)
# 드라이버 옵션
options = Options()
# options.add_argument("--headless=new")
options.add_argument("disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

driver.get(envs.TEMU_BEST_SELLER_URL)
time.sleep(5.5)

SEARCH_KEYWORD = {
    1:"패션의류",
    2:"생활/건강",
}

def scrape_temu_data(driver, worksheet, search_keyword ,start_cell):
    print("Scraping temu data")

    # TODO: 베스트셀러 링크를 들어가면 로그인 or 네트워크로 막힘 개선 필요함
    # 1) 베스트셀러 클릭
    # seller_btn = WebDriverWait(driver, 15).until(
    #     EC.element_to_be_clickable((By.CSS_SELECTOR, envs.TEMU_SELLER_BTN))
    # )
    # driver.execute_script("arguments[0].click();", seller_btn)

    # TODO: 검색창에 검색을하고 들어가도 로그인 or 네트워크로 막힘 개선 필요함
    # search_fashion = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.CLASS_NAME, envs.TEMU_SEARCH_INPUT))
    # )
    # search_fashion.send_keys(search_keyword)
    # search_fashion.send_keys(Keys.RETURN)

    records = []
    # 스크롤 다운 (lazy loading 방지)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    title_items = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, envs.TEMU_TITLE_TAG))
    )
    for title in title_items:
        records.append(title.text)

    print(records)
    return records
scrape_temu_data(driver, worksheet, SEARCH_KEYWORD[1] , "A3")

driver.quit()