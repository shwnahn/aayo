from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from crawler import *  # setup_driver, save_data 불러옴
import time  # time.sleep 쓰려고

def click_more_button_toms(driver, by, selector):
    while True:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            more_button = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((by, selector))
            )
            # "더보기" 버튼이 disabled 상태인지 확인
            if more_button.get_attribute('disabled'):
                print("'더보기' 버튼이 disabled 상태입니다.")
                time.sleep(0.5)
                driver.execute_script("window.scrollTo(0, 500);")
                time.sleep(0.5)
                break

            driver.execute_script("arguments[0].click();", more_button)
            # more_button.send_keys('Enter')
            print('더보기 BUTTON CLICKED')
            time.sleep(0.5)
        except TimeoutException:
            print("더 이상 '더보기' 버튼이 없습니다.")
            time.sleep(0.5)
            driver.execute_script("window.scrollTo(0, 500);")
            time.sleep(0.5)
            break

def crawl_toms():
    # 카페명과 메뉴 URL
    cafe_name = 'toms'
    url = "https://www.tomntoms.com/menu/drink"

    # 웹드라이버 설정
    driver = setup_driver()
    crawled_items = set()

    try:
        driver.get(url)
        driver.implicitly_wait(3)
        data = []
        note =''
        
        categories = driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')
        for i in range(len(categories) - 1):
            categories[i].click()
            categories[i+1].click()
            category = categories[i+1].get_attribute('id')
            print(f'# {category}')
            time.sleep(0.5)

            # 스크롤 내림
            click_more_button_toms(driver, By.XPATH, '//*[@id="root"]/section[5]/div[2]/button')

            menu_items = driver.find_elements(By.CSS_SELECTOR, 'div.relative.w-full')
            # for문으로 메뉴 전체 순회하며 'menu_name', 'image_url'를 가져와서 data 리스트에 추가하기
            for item in menu_items:
                menu_name = item.find_element(By.CSS_SELECTOR, 'span.tracking-wider').text
                image_url = item.find_element(By.TAG_NAME, 'img').get_attribute('src')
                
                print(f"메뉴명: {menu_name}")
                print(f"이미지 URL: {image_url}")

                data.append({
                        "menu_name": menu_name,
                        "image_url": image_url,
                        "category": category,
                        "note": note,
                    })
                print(f"[{category}] {menu_name} - {note}")
                print(image_url)
                
        save_data(cafe_name, data)

    finally:
        driver.quit()

# 이 코드 실행 시 크롤링 함수 호출
if __name__ == "__main__":
    crawl_toms()