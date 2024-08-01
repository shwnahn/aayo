from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_starbucks_menu():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://www.starbucks.co.kr/menu/drink_list.do")
    
    # 페이지가 완전히 로드될 때까지 기다립니다
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "ul.product_list"))
    )

    # 스크롤을 천천히 내려 모든 항목이 로드되도록 합니다
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    menu_items = driver.find_elements(By.CSS_SELECTOR, "ul.product_list li")
    menus = []
    for item in menu_items:
        try:
            name = item.find_element(By.CSS_SELECTOR, "dd").text
            img_url = item.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
            menus.append({'name': name, 'image': img_url})
        except:
            continue

    driver.quit()
    return menus