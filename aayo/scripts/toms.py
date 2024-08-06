from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from crawler import *  # setup_driver, save_data 불러옴
import time  # time.sleep 쓰려고

def crawl_toms():
    # 카페명과 메뉴 URL
    cafe_name = 'toms'
    url = "https://www.tomntoms.com/menu/drink"

    # 웹드라이버 설정
    driver = setup_driver()

    try:
        driver.get(url)
        driver.implicitly_wait(3)

        data = []
        crawled_items = set()  # 중복된 항목을 저장하는 집합(확인하려고)

        while True:
            menu_items = driver.find_elements(By.CSS_SELECTOR, 'div.relative.w-full')

            # for문으로 메뉴 전체 순회하며 'menu_name', 'image_url'를 가져와서 data 리스트에 추가하기
            for item in menu_items:
                menu_name = item.find_element(By.CSS_SELECTOR, 'span.tracking-wider').text
                image_url = item.find_element(By.TAG_NAME, 'img').get_attribute('src')

                # 이미 크롤링된 항목이 아닌 경우에만 추가
                if (menu_name, image_url) not in crawled_items:
                    data.append({'menu_name': menu_name, 'image_url': image_url})
                    crawled_items.add((menu_name, image_url))
                    #print(menu_name, image_url)

            try:
                more_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/section[5]/div[2]/button'))
                )
                driver.execute_script("arguments[0].click();", more_button)
                time.sleep(1)  
            except TimeoutException:
                print("더 이상 '더보기' 버튼이 없습니다.")
                break

        save_data(cafe_name, data)

    finally:
        driver.quit()

# 이 코드 실행 시 크롤링 함수 호출
if __name__ == "__main__":
    crawl_toms()
