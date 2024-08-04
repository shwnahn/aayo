from selenium.webdriver.common.by import By
from crawler import * # setup_driver, save_data 불러옴

def crawl_starbucks():
    """
    스타벅스 웹사이트를 크롤링하여 메뉴명과 이미지 URL을 추출하는 함수.
    """
    # 카페명과 메뉴URL
    cafe_name = 'starbucks'
    url = "https://www.starbucks.co.kr/menu/drink_list.do"

    # 웹드라이버 설정
    driver = setup_driver()

    try:
        # 크롤링할 페이지 열기
        driver.get(url)

        # 페이지 소스 로딩 대기 (최대 3초)
        driver.implicitly_wait(3)

        # 메뉴명과 이미지 URL 추출
        data = []
        menu_items = driver.find_elements(By.CSS_SELECTOR, "li.menuDataSet")
        for item in menu_items:
            menu_name = item.find_element(By.TAG_NAME, 'dd').text
            image_url = item.find_element(By.TAG_NAME, 'img').get_attribute('src')
            data.append({
                "menu_name": menu_name,
                "image_url": image_url,
            })
        
        # JSON 파일로 저장
        save_data(cafe_name, data)
    finally:
        # 크롤링 성공여부 상관없이 무조건 실행되어 웹드라이버를 종료
        driver.quit()

# 이 코드 실행 시 crawl_starbucks 함수 호출
if __name__ == "__main__":
    crawl_starbucks()