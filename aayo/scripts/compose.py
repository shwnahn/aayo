from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from crawler import *
import time

def crawl_compose():
    # 카페명과 메뉴URL
    cafe_name = 'compose'
    url = "https://composecoffee.com/menu"

    # 웹드라이버 설정
    driver = setup_driver()

    try:
        # 크롤링할 페이지 열기
        driver.get(url)
        # 페이지 소스 로딩 대기 (최대 3초)
        driver.implicitly_wait(3)

        data = []
        
        # 페이지 버튼의 개수를 확인합니다.
        page_buttons = driver.find_elements(By.CSS_SELECTOR, "#bd_152_0 > nav > ul > li > a")
        total_pages = len(page_buttons)

        for page in range(1, total_pages - 3): 
            # 현재 음료가 6페이지까지만 있어서 부득이하게 하드코딩... 도넛 두 개 딸려옴;;
            print(f"페이지 {page} 크롤링 중...")
            
            if page > 1:
                # 현재 페이지 버튼 클릭 (첫 페이지는 클릭할 필요 없음)
                page_button = driver.find_element(By.CSS_SELECTOR, f"#bd_152_0 > nav > ul > li:nth-child({page}) > a")
                driver.execute_script("arguments[0].click();", page_button)
                time.sleep(2)  # 페이지 로딩 대기

            # 메뉴 아이템 찾기
            menu_items = driver.find_elements(By.CSS_SELECTOR, "#masonry-container > div")
            
            # for문으로 메뉴 전체 순회하며 'menu_name', 'image_url'를 가져와서 data 리스트에 추가하기
            for item in menu_items:
                try:
                    menu_name = item.find_element(By.CSS_SELECTOR, 'h3').text
                    image_url = item.find_element(By.CSS_SELECTOR, '#rthumbnail > img').get_attribute('src')
                    
                    print(f"메뉴명: {menu_name}, 이미지 URL: {image_url}") # 크롤링 잘 되는지 테스트용

                    # menu_name, image_url을 data 리스트에 하나씩 추가
                    data.append({
                        "menu_name": menu_name,
                        "image_url": image_url,
                    })
                except NoSuchElementException as e:
                    print(f"메뉴 항목 처리 중 오류 발생: {e}")
        
        # JSON 파일로 저장
        save_data(cafe_name, data)
        # print(f"총 {len(data)}개의 메뉴 항목을 크롤링했습니다.")

    except Exception as e:
        print(f"크롤링 중 오류 발생: {e}")
    finally:
        # 크롤링 성공여부 상관없이 무조건 실행되어 웹드라이버를 종료
        driver.quit()

# 이 코드 실행 시 크롤링 함수 호출
if __name__ == "__main__":
    crawl_compose()