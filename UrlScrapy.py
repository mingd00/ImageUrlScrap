from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import json

# JSON 파일 읽기
with open('uni_map_data.json', 'r', encoding='utf-8') as file:
    universities = json.load(file)

def update_chrome():
    global driver
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument('lang=ko_KR')
    chrome_options.add_argument('disable-gpu')
    # chrome_options.add_argument("headless")
    chrome_options.add_experimental_option("excludeSwitches", ['enable-logging'])
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)  # 페이지 로딩을 위해 최대 10초 대기

def create_json_file(result_data):
    with open("image_url.json", "w", encoding="utf-8") as json_file:
        json.dump(result_data, json_file, indent=4, ensure_ascii=False)

def search_data(university):
    try:
        wait = WebDriverWait(driver, 20)  # 요소가 나타날 때까지 최대 20초 동안 대기
        elem = driver.find_element(By.NAME, "q")
        elem.send_keys(university + " 홈페이지")
        elem.send_keys(Keys.RETURN)

        home_url = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[jsname='UWckNb']"))).get_attribute("href")
        return home_url
    except (TimeoutException, NoSuchElementException):
        return None  # 요소를 찾지 못하거나 타임아웃 발생시 None 반환

def open_page(page_url):
    driver.get(page_url)

if __name__ == "__main__":
    result_data = []
    update_chrome()
    for university in universities:
        open_page('https://www.google.com/')
        university_name = university["university"]
        home_url = search_data(university_name)
        if home_url:
            university["home_url"] = home_url
            create_json_file(universities)  # 새 URL을 포함하여 JSON 파일 업데이트
        else:
            print(f"Homepage URL not found for {university_name}")
