from selenium.webdriver.common.by import By # 요소 찾을 때 필요함
from crawler import * # setup_driver, save_data 불러옴
import time # time.sleep 쓰려고

def crawl_cafename():
    # 카페명과 메뉴URL
    cafe_name = 'cafename'
    url = ""

    # 웹드라이버 설정
    driver = setup_driver()

    try:
        # 크롤링할 페이지 열기
        driver.get(url)
        # 페이지 소스 로딩 대기 (최대 3초)
        driver.implicitly_wait(3)

        ###### 메뉴명과 이미지 URL 추출 - 카페마다 코드 다르게 할 부분! ######
        data = []
        menu_items = driver.find_elements(By.CSS_SELECTOR, "li.menuDataSet")
        
        # for문으로 메뉴 전체 순회하며 'menu_name', 'image_url'를 가져와서 data 리스트에 추가하기
        for item in menu_items:
            menu_name = item.find_element(By.TAG_NAME, 'dd').text
            image_url = item.find_element(By.TAG_NAME, 'img').get_attribute('src')
            
            print(menu_name, image_url) # 이렇게 테스트해보면서 하면 좋다.

            # menu_name, image_url을 data 리스트에 하나씩 추가
            data.append({
                "menu_name": menu_name,
                "image_url": image_url,
            })
        
        # JSON 파일로 저장
        save_data(cafe_name, data)
    finally:
        # 크롤링 성공여부 상관없이 무조건 실행되어 웹드라이버를 종료
        driver.quit()

# 이 코드 실행 시 크롤링 함수 호출
if __name__ == "__main__":
    crawl_cafename()