from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import json

# JSON 파일 읽기
with open('uni_map_data.json', 'r', encoding='utf-8') as file:
    universities = json.load(file)

# driver 셋팅 API
def update_chrome():
    global driver
    
    # 자동 꺼짐 방지 -> vscode에서 개발할 땐 f5말고 run python file로 실행
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True) 
    chrome_options.add_argument('lang=ko_KR')  # 사용언어 한국어
    chrome_options.add_argument('disable-gpu')  # 하드웨어 가속 안함
    # chrome_options.add_argument("headless") # 백그라운드 실행
    chrome_options.add_experimental_option("excludeSwitches", ['enable-logging'])  # 불필요한 에러 메세지 삭제 
    driver = webdriver.Chrome(options=chrome_options) # 크롬 드라이버 생성
    driver.implicitly_wait(100) # 페이지 로딩이 완료될 떼까지 기다리는 코드 (10초 설정)
    
    return

def create_json_file(result_data):
    # 추출한 데이터를 JSON 파일로 저장
    with open("url.json", "w", encoding="utf-8") as json_file:
        json.dump(result_data, json_file, indent=4, ensure_ascii=False)
        
# data 검색
def search_data(university):
    wait = WebDriverWait(driver, 10)
    elem = driver.find_element(By.NAME, "q")
    elem.send_keys(university + " 홈페이지")
    elem.send_keys(Keys.RETURN)
    
    driver.implicitly_wait(100)
    # 검색 후 화면이 로드되기를 기다리고 홈페이지 url 저장
    home_url = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[jsname='UWckNb']"))).get_attribute("href")
    return home_url

    
# url을 매개변수로 페이지 오픈 API
def open_page(page_url):
    driver.get(page_url)
    driver.implicitly_wait(100)
    return

if __name__ == "__main__":
    result_data = []
    update_chrome()
    # 사이트 접속
    for university in universities:
            open_page('https://www.google.com/')
            university_name = university["university"]
            home_url = search_data(university_name)
            if home_url:
                university["home_url"] = home_url
                #json파일 생성
                create_json_file(universities)
            else:
                print(f"Logo not found for {university_name}")
            driver.implicitly_wait(100)

    

    