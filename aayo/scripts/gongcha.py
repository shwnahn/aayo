from selenium.webdriver.common.by import By # 요소 찾을 때 필요함
from crawler import * # setup_driver, save_data 불러옴
import time # time.sleep 쓰려고

def save_index(driver):
    driver.get("https://www.gong-cha.co.kr/brand/menu/product.php?c=001001")
    print("접속성공")
    driver.implicitly_wait(3)
    index_list = []
    indexes = driver.find_elements(By.CSS_SELECTOR, 'div.pro_list_tab > ul > li > a')
    for index in indexes:
        url = index.get_attribute('href')
        category = index.find_element(By.TAG_NAME, 'span').text
        index_list.append({
            "url": url,
            "category": category
        })
    print(index_list)
    return index_list


def crawl_gongcha():
    # 카페명과 메뉴URL
    cafe_name = 'gongcha'
    # 웹드라이버 설정 
    driver = setup_driver()

    try: 
        data = []
        index_list = save_index(driver)
        driver.implicitly_wait(3)
        print("# index_list 함수 구동 완료")
        for entry in index_list:
            url = entry["url"]
            category = entry["category"]
            note = ''
            print("url 오픈...")
            print(url)
            # 크롤링할 페이지 열기
            driver.get(url)
            # 페이지 소스 로딩 대기 (최대 3초)
            driver.implicitly_wait(3)

            ###### 메뉴명과 이미지 URL 추출 - 카페마다 코드 다르게 할 부분! ######
            
            menu_items = driver.find_elements(By.CSS_SELECTOR, "div#contents div:not(.pro_list_tab) ul > li")
            
            # for문으로 메뉴 전체 순회하며 'menu_name', 'image_url'를 가져와서 data 리스트에 추가하기
            for item in menu_items:
                menu_name = item.find_element(By.CSS_SELECTOR, 'span.txt').text
                image_url = item.find_element(By.CSS_SELECTOR, 'span.img > img').get_attribute('src')

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
    crawl_gongcha()