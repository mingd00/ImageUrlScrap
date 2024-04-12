from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
import json

# JSON 파일 읽기
with open('image_url.json', 'r', encoding='utf-8') as file:
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
    driver.implicitly_wait(10)

def create_json_file(result_data):
    with open("image_url.json", "w", encoding="utf-8") as json_file:
        json.dump(result_data, json_file, indent=4, ensure_ascii=False)

def search_data(university):
    try:
        wait = WebDriverWait(driver, 20)
        elem = driver.find_element(By.NAME, "q")
        elem.send_keys(university + " 로고 jpg")
        elem.send_keys(Keys.RETURN)
        
        element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".mNsIhb")))
        actions = ActionChains(driver)
        actions.move_to_element(element).click().perform()
        
        image_url = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".sFlh5c.pT0Scc"))).get_attribute("src")
        return image_url
    except (TimeoutException, NoSuchElementException):
        # 요소를 찾지 못하거나 타임아웃이 발생한 경우 None을 반환
        return None

def open_page(page_url):
    driver.get(page_url)

if __name__ == "__main__":
    result_data = []
    update_chrome()
    for university in universities:
        open_page('https://www.google.com/imghp?hl=en&ogbl')
        university_name = university["university"]
        logo_url = search_data(university_name)
        if logo_url:
            university["logo"] = logo_url
            create_json_file(universities)
        else:
            print(f"Logo not found for {university_name}")
