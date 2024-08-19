from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from crawler import *
import time

def save_index(driver):
    driver.get("https://www.coffeebeankorea.com/menu/list.asp?category=11")
    print("# 접속성공")
    driver.implicitly_wait(3)
    index_list = []
    indexes = driver.find_elements(By.CSS_SELECTOR, 'ul.lnb_wrap2 > li:nth-child(1) > ul > li > a')
    for i, index in enumerate(indexes):
        # 마지막 요소(엑스트라)를 건너뛰기
        if i == len(indexes) - 1:
            break
        url = index.get_attribute('href')
        category = index.text
        index_list.append({
            "url": url,
            "category": category
        })

    print(index_list)
    return index_list

def crawl_bean():
    cafe_name = 'bean'

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
            
            while True: # (2) 페이지 순회
                print("# 웹 페이지 순회")
                pages = driver.find_elements(By.CSS_SELECTOR, "div.paging > a")

                # (3) 메뉴 아이템 순회하며 정보 받아오기
                print("# 메뉴 아이템 순회")
                menu_items = driver.find_elements(By.CSS_SELECTOR, "ul.menu_list > li")
                for item in menu_items:
                    item.get_attribute('innerHTML')
                    menu_name = item.find_element(By.CSS_SELECTOR, 'dl.txt > dt > span.kor').text
                    image_url = item.find_element(By.TAG_NAME, 'img').get_attribute('src')
                    note = item.find_element(By.CSS_SELECTOR, 'dl.txt > dd').text

                    if menu_name:
                        data.append({
                            "menu_name": menu_name,
                            "image_url": image_url,
                            "category": category,
                            "note": note,
                        })
                        print(f"[{category}] {menu_name} - {note}")
                        print(image_url)

                # 만약 마지막 페이지가 'on'(활성화) 되어있다면 While문 break
                if 'on' in pages[-1].get_attribute('class'):
                    print("## last page")
                    # 1번
                    break

                # 마지막 페이지가 활성화되어있지 않다면 next button 클릭하기
                next_button = driver.find_element(By.CSS_SELECTOR, "div.paging > a.next")
                print("# next page")
                next_button.click()
                driver.implicitly_wait(3)
        
        save_data(cafe_name, data)
    finally:
        driver.quit()

if __name__ == "__main__":
    crawl_bean()