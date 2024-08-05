from selenium.webdriver.common.by import By # 요소 찾을 때 필요함
from selenium.webdriver.common.keys import Keys
from crawler import * # setup_driver, save_data 불러옴
import time # time.sleep 쓰려고

def crawl_twosome():
    # 카페명과 메뉴URL
    cafe_name = 'twosome'
    url = "https://mo.twosome.co.kr/mn/menuInfoList.do"

    # 웹드라이버 설정
    driver = setup_driver()

    try:
        driver.get(url) # 크롤링할 페이지 열기
        driver.implicitly_wait(3) # 페이지 소스 로딩 대기 (최대 3초)
        drinks_btn = driver.find_element(By.CSS_SELECTOR, 'a[name="grtNm"][grtval="1"][value="1"]')
        drinks_btn.click()
        driver.implicitly_wait(3)

        ###### 메뉴명과 이미지 URL 추출 - 카페마다 코드 다르게 할 부분! ######
        data = []

        category_btn_coffee = driver.find_element(By.CSS_SELECTOR, 'li[name="midLi"] > a[name="midNm"][midval="01"][value="01"]')
        category_btn_coffee.click()
        driver.implicitly_wait(3)
        
        # 스크롤을 무한 반복하여 맨 밑에 도달할 때까지
        while True:
            # 현재 페이지 높이 저장
            last_height = driver.execute_script("return document.body.scrollHeight")
            # 스크롤을 맨 아래로 내림
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # 새로운 콘텐츠 로드 시간 대기
            time.sleep(0.5)
            # 새로운 페이지 높이 저장
            new_height = driver.execute_script("return document.body.scrollHeight")
            # 새로운 페이지 높이와 이전 페이지 높이를 비교하여 끝에 도달했는지 확인
            if new_height == last_height:
                break  # 더 이상 새로운 콘텐츠가 로드되지 않으면 반복 종료

        menu_items = driver.find_elements(By.CSS_SELECTOR, 'ul.ui-goods-list-default li')
        print(menu_items)
        
        # for문으로 메뉴 전체 순회하며 'menu_name', 'image_url'를 가져와서 data 리스트에 추가하기
        for item in menu_items:
            menu_name = item.find_element(By.CSS_SELECTOR, 'p.menu-title').text
            if menu_name:
                print(menu_name)
                image_url = item.find_element(By.CSS_SELECTOR, 'div.thum-img > img').get_attribute('src')
                print(image_url) # 이렇게 테스트해보면서 하면 좋다.
            else:
                print("menu_name is None")
                continue

        #     # menu_name, image_url을 data 리스트에 하나씩 추가
        #     data.append({
        #         "menu_name": menu_name,
        #         "image_url": image_url,
        #     })


        category_btn_beverage = driver.find_element(By.CSS_SELECTOR, 'li[name="midLi"] > a[name="midNm"][midval="02"][value="02"]')
        category_btn_beverage.click()
        time.sleep(1)

        category_btn_tea = driver.find_element(By.CSS_SELECTOR, 'li[name="midLi"] > a[name="midNm"][midval="03"][value="03"]')
        category_btn_tea.click()
        time.sleep(1)

    
        
        
        # # JSON 파일로 저장
        # save_data(cafe_name, data)
    finally:
        # 크롤링 성공여부 상관없이 무조건 실행되어 웹드라이버를 종료
        driver.quit()

# 이 코드 실행 시 크롤링 함수 호출
if __name__ == "__main__":
    crawl_twosome()