from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from crawler import *  # setup_driver, save_data 불러옴
import time  # time.sleep 쓰려고
import re

def crawl_hollys(driver, url):
    data = []

    try:
        driver.get(url)
        driver.implicitly_wait(5)  # 5초 동안 대기
        
        menu_items = driver.find_elements(By.CSS_SELECTOR, "ul.menu_list01 > li")

        for item in menu_items:
            menu_name = item.find_element(By.CSS_SELECTOR, 'ul.menu_list01 > li > a').text
            image_url = item.find_element(By.CSS_SELECTOR, 'ul.menu_list01 > li > a > img').get_attribute('src')
            
            menu_name = menu_name.replace('\n', ' ')  # \n을 공백으로 대체
            menu_name = re.sub(r'<br\s*/?>', ' ', menu_name)  # <br> 태그를 공백으로 대체
            
            if "빙수" not in menu_name:
                print(menu_name, image_url)
                data.append({
                    "menu_name": menu_name,
                    "image_url": image_url,
                })

            try:
                more_button = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.more_menu > a'))
                )
                driver.execute_script("arguments[0].click();", more_button)
                time.sleep(1)  
            except TimeoutException:
                print("더 이상 '더보기' 버튼이 없습니다.")
                break

    except Exception as e:
        print(f"크롤링 중 오류 발생: {e}")

    return data

def main():
    cafe_name = 'hollys'
    all_data = []

    urls = [
        "https://www.hollys.co.kr/menu/espresso.do",
        "https://www.hollys.co.kr/menu/signature.do",
        "https://www.hollys.co.kr/menu/hollyccino.do",
        "https://www.hollys.co.kr/menu/juice.do",
        "https://www.hollys.co.kr/menu/tea.do"
    ]

    driver = setup_driver()

    try:
        for url in urls:
            data = crawl_hollys(driver, url)
            all_data.extend(data)
            time.sleep(2) # 웹사이트 부하 방지

        save_data(cafe_name, all_data)

    except Exception as e:
        print(f"전체 크롤링 과정 중 오류 발생: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()