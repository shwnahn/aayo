from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from crawler import * # setup_driver, save_data 불러옴
import time # time.sleep 쓰려고

def crawl_mega():
    # 카페명과 메뉴 URL
    cafe_name = 'mega'
    url = "https://www.mega-mgccoffee.com/menu/?menu_category1=1&menu_category2=1"

    # 웹드라이버 설정
    driver = setup_driver()

    try:
        driver.get(url)
        driver.implicitly_wait(3)

        data = []
        note = ''

        # 첫 번째로 '전체 상품 보기' 체크박스 해제
        all_products_checkbox = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]')
        driver.execute_script("arguments[0].click();", all_products_checkbox)
        time.sleep(1)  # 페이지 로드 시간 대기

        # 모든 카테고리 가져오기
        categories = driver.find_elements(By.CLASS_NAME, 'checkbox_wrap')

        # '전체 상품 보기'를 제외한 나머지 카테고리 순회 (1부터 시작)
        for category_element in categories[1:]:
            checkbox_input = category_element.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]')
            checkbox_label = category_element.find_element(By.CSS_SELECTOR, 'div.checkbox_text')
            category = checkbox_label.text.strip()

            # 카테고리 클릭
            driver.execute_script("arguments[0].click();", checkbox_input)
            time.sleep(1)  # 페이지 로드 시간 대기

            # 현재 선택된 카테고리에서 메뉴 크롤링
            menu_items = driver.find_elements(By.CSS_SELECTOR, "#menu_list > li")

            for item in menu_items:
                menu_name = item.find_element(By.CSS_SELECTOR, 'div.cont_text_title > div.text1 > b').text
                image_url = item.find_element(By.TAG_NAME, 'img').get_attribute('src')
                data.append({
                    'menu_name': menu_name,
                    'image_url': image_url,
                    'category': category,
                    'note': note,
                })
                print(f"[{category}] {menu_name} - {note}")
                print(image_url)

            try:
                more_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "#board_page > li > a.board_page_next"))
                )
                driver.execute_script("arguments[0].click();", more_button)
                time.sleep(1)
            except TimeoutException:
                print("더 이상 '다음' 버튼이 없습니다.")
            
            # 카테고리 체크박스 해제
            driver.execute_script("arguments[0].click();", checkbox_input)
            time.sleep(1)  # 페이지 로드 시간 대기

        save_data(cafe_name, data)

    finally:
        driver.quit()

# 이 코드 실행 시 크롤링 함수 호출
if __name__ == "__main__":
    crawl_mega()