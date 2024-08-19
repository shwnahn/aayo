from selenium.webdriver.common.by import By # 요소 찾을 때 필요함
from crawler import * # setup_driver, save_data 불러옴
import time # time.sleep 쓰려고


def save_index(driver):
    driver.get("https://www.yogerpresso.co.kr/menu/menu.html")
    print("접속성공")
    driver.implicitly_wait(3)
    index_list = []
    indexes = driver.find_elements(By.CSS_SELECTOR, "div.tab-list > a")
    for index in indexes:
        url = index.get_attribute('href')
        category = index.get_attribute('innerText')
        if category == 'ALL MENU':
            #  or category == '디저트'
            continue
        index_list.append({
            "url": url,
            "category": category
        })
    print(index_list)
    return index_list


def crawl_yoger():
    # 카페명과 메뉴URL
    cafe_name = 'yoger'

    # 웹드라이버 설정 
    driver = setup_driver()

    try:
        data = []

        index_list = save_index(driver)
        for entry in index_list:
            url = entry["url"]
            category = entry["category"]
            note = ''
            print(f'# 카테고리 순회 - {category}')
            driver.get(url)
            driver.implicitly_wait(3)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            menu_items = driver.find_elements(By.CSS_SELECTOR, "ul.gallery-custom-list > li")
            
            # for문으로 메뉴 전체 순회하며 'menu_name', 'image_url'를 가져와서 data 리스트에 추가하기
            for item in menu_items:
                menu_name = item.find_element(By.CSS_SELECTOR, 'a > p.text').get_attribute('innerText')
                image_url = item.find_element(By.CSS_SELECTOR, 'div.img-bx > img').get_attribute('src')
                
                print(menu_name, image_url) # 이렇게 테스트해보면서 하면 좋다.

                if menu_name:
                    data.append({
                        "menu_name": menu_name,
                        "image_url": image_url,
                        "category": category,
                        "note": note,
                    })
                    print(f"[{category}] {menu_name} - {note}")
                    print(image_url)
            
        # JSON 파일로 저장
        save_data(cafe_name, data)
    finally:
        # 크롤링 성공여부 상관없이 무조건 실행되어 웹드라이버를 종료
        driver.quit()

# 이 코드 실행 시 크롤링 함수 호출
if __name__ == "__main__":
    crawl_yoger()