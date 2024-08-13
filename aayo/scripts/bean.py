from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from crawler import *
import time

def crawl_bean():
    cafe_name = 'bean'
    base_url = "https://www.coffeebeankorea.com/menu/list.asp?category="

    driver = setup_driver()

    try:
        data = []
        categories = ['11', '12', '13', '14', '17', '18', '24', '26']

        # 코드 구조:
            # (1) 카테고리 순회
                # (2) 페이지 순회
                    # (3) 메뉴 아이템 순회하며 정보 받아오기
                
        for category in categories : # (1) 카테고리 순회
            print("# 카테고리 순회")
            url = base_url + category
            driver.get(url)
            driver.implicitly_wait(3)
            
            while True: # (2) 페이지 순회
                print("# 웹 페이지 순회")

                pages = driver.find_elements(By.CSS_SELECTOR, "div.paging > a")

                # (3) 메뉴 아이템 순회하며 정보 받아오기
                print("# 메뉴 아이템 순회")
                menu_items = driver.find_elements(By.CSS_SELECTOR, "ul.menu_list > li")
                for item in menu_items:
                    try:
                        menu_name = item.find_element(By.CSS_SELECTOR, 'span.kor').text
                        print(menu_name)
                        image_url = item.find_element(By.TAG_NAME, 'img').get_attribute('src')
                        print(image_url)

                        data.append({
                            "menu_name": menu_name,
                            "image_url": image_url,
                        })

                    except Exception as e:
                        print(f"Error processing menu item: {str(e)}")

                # 만약 마지막 페이지가 'on'(활성화) 되어있다면 While문 break
                if 'on' in pages[-1].get_attribute('class'):
                    print("## last page")
                    # 1번
                    break

                # 마지막 페이지가 활성화되어있지 않다면 next button 클릭하기
                next_button = driver.find_element(By.CSS_SELECTOR, "div.paging > a.next")
                print("next page")
                next_button.click()
                driver.implicitly_wait(3)
            
        
        save_data(cafe_name, data)
    finally:
        driver.quit()

if __name__ == "__main__":
    crawl_bean()