from selenium.webdriver.common.by import By # 요소 찾을 때 필요함
from selenium.webdriver.common.keys import Keys
from crawler import * # setup_driver, save_data, scroll_down
import time # time.sleep 쓰려고


def update_data(data, driver, category):
    menu_items = driver.find_elements(By.CSS_SELECTOR, 'ul.ui-goods-list-default li:not(.next)')

    # for문으로 메뉴 전체 순회하며 'menu_name', 'image_url'를 가져와서 data 리스트에 추가하기
    for item in menu_items:
        menu_name = item.find_element(By.CSS_SELECTOR, 'p.menu-title').text
        image_url = item.find_element(By.CSS_SELECTOR, 'div.thum-img > img').get_attribute('src')
        note = ''
        # menu_name, image_url을 data 리스트에 하나씩 추가
        data.append({
            "menu_name": menu_name,
            "image_url": image_url,
            "category": category,
            "note": note,
        })
        
        print(f"[{category}] {menu_name} - {note}")
        print(image_url)

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
        category_coffee = category_btn_coffee.text
        category_btn_coffee.click()
        driver.implicitly_wait(3)
        
        scroll_down(driver)
        update_data(data, driver,category_coffee)

        category_btn_beverage = driver.find_element(By.CSS_SELECTOR, 'li[name="midLi"] > a[name="midNm"][midval="02"][value="02"]')
        category_beverage = category_btn_beverage.text
        category_btn_beverage.click()
        time.sleep(1)
        scroll_down(driver)
        update_data(data, driver,category_beverage)

        category_btn_tea = driver.find_element(By.CSS_SELECTOR, 'li[name="midLi"] > a[name="midNm"][midval="03"][value="03"]')
        category_tea = category_btn_tea.text
        category_btn_tea.click()
        time.sleep(1)
        scroll_down(driver)
        update_data(data, driver, category_tea)
        
        # JSON 파일로 저장
        save_data(cafe_name, data)
    finally:
        # 크롤링 성공여부 상관없이 무조건 실행되어 웹드라이버를 종료
        driver.quit()

# 이 코드 실행 시 크롤링 함수 호출
if __name__ == "__main__":
    crawl_twosome()