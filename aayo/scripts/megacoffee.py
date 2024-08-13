from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager # Chrome driver 자동 업데이트
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import json
import os

# 브라우저 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 불필요한 에러메시지 노출 방지
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# Chrome driver Manager를 통해 크롬 드라이버 자동 설치
service = Service(excutable_path=ChromeDriverManager().install()) 
driver = webdriver.Chrome(service=service, options = chrome_options)

data = []
url = "https://www.starbucks.co.kr/menu/drink_list.do"
driver.get(url)
#페이지 소스 로딩 대기 (최대 3초)
driver.implicitly_wait(3)

menu_items = driver.find_elements(By.CSS_SELECTOR, 'li.menuDataSet')
# 메뉴명과 이미지 URL 추출
for item in menu_items:
    menu_name = item.find_element(By.TAG_NAME, 'dd').text
    image_url = item.find_element(By.TAG_NAME, 'img').get_attribute('src')
    data.append({
        "menu_name": menu_name,
        "image_url": image_url,
    })

driver.quit()

cafe_name = 'starbucks'
# 저장할 파일 경로 설정
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', f'{cafe_name}.json')

# 디렉토리가 없는 경우 생성
os.makedirs(os.path.dirname(file_path), exist_ok=True)

# JSON 파일로 저장
with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)