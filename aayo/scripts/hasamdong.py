from selenium.webdriver.common.by import By # 요소 찾을 때 필요함
from crawler import *
import time # time.sleep 쓰려고
import re

def crawl_hasamdong():
    # 카페명과 메뉴URL
    cafe_name = 'hasamdong'
    url = "https://www.hasamdongcoffee.com/menu_list.php"

    # 웹드라이버 설정
    driver = setup_driver()

    try:
        # 크롤링할 페이지 열기
        driver.get(url)
        # 페이지 소스 로딩 대기 (최대 3초)
        driver.implicitly_wait(3)
        scroll_down(driver)

        ###### 메뉴명과 이미지 URL 추출 - 카페마다 코드 다르게 할 부분! ######
        data = []
        list_groups = driver.find_elements(By.CSS_SELECTOR,"div.list-group")
        for list_group in list_groups:
            print(f"##### list_group 순회 중... #####")
            category = list_group.find_element(By.CSS_SELECTOR, "h3.list-title").text
            menu_items = list_group.find_elements(By.CSS_SELECTOR,"ul.list-type-menu > li")
            # for문으로 메뉴 전체 순회하며 'menu_name', 'image_url'를 가져와서 data 리스트에 추가하기
            for item in menu_items:
                menu_name = item.find_element(By.CSS_SELECTOR, 'div.detail > p:nth-child(1)').text
                note = item.find_element(By.CSS_SELECTOR, 'div.detail > p:nth-child(2)').text
                image_element = item.find_element(By.CLASS_NAME, 'thumb').get_attribute('style')
                relative_url = re.search(r'url\("(.+?)"\)', image_element).group(1)
                image_url = "https://www.hasamdongcoffee.com" + relative_url

                #menu_name, image_url을 data 리스트에 하나씩 추가
                if menu_name:
                    data.append({
                        "menu_name": menu_name,
                        "image_url": image_url,
                        "category": category,
                        "note": note,
                    })
                    print(f"[{category}] {menu_name} - {note}")
                    print(image_url)
                else:
                    break
        # JSON 파일로 저장
        save_data(cafe_name, data)
        print(f"### {cafe_name} 데이터 저장 완료! ###")
    finally:
        # 크롤링 성공여부 상관없이 무조건 실행되어 웹드라이버를 종료
        driver.quit()

# 이 코드 실행 시 크롤링 함수 호출
if __name__ == "__main__":
    crawl_hasamdong()