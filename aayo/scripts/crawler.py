from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager # Chrome driver 자동 업데이트
import json
import os

def setup_driver():
    """
    Selenium 웹드라이버를 설정하고, driver 객체를 반환하는 함수.
    """
    # 드라이버 설정 - Options
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True) # 브라우저 꺼짐 방지
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"]) # 불필요한 에러메시지 노출 방지
    # 드라이버 설정 - Service
    service = Service(excutable_path=ChromeDriverManager().install()) #Chrome driver Manager를 통해 크롬 드라이버 자동 설치
    driver = webdriver.Chrome(service=service, options = chrome_options)

    return driver

def save_data(cafe_name, data):
    """
    데이터를 JSON 파일로 저장하는 함수.
    Parameters:
        cafe_name (str): 저장할 JSON 파일의 이름에 사용할 카페명
        data (list): 저장할 데이터 목록 (메뉴명, 이미지 URL)
    """
    # 저장할 파일 경로 설정
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', f'{cafe_name}.json')
    # 디렉토리가 없는 경우 파일 생성
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    # 지정된 파일 경로에 JSON 파일로 저장
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)