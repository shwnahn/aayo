from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.by import By
from crawler import *  # setup_driver, save_data 불러옴
import time
import re

def save_index(driver):
    driver.get("https://www.hollys.co.kr/menu/espresso.do")
    print("# 접속성공")
    driver.implicitly_wait(3)
    index_list = []
    indexes = driver.find_elements(By.CSS_SELECTOR, 'ul.lnb > li > a')
    for i, index in enumerate(indexes):
        # 마지막 요소 2개(MD상품, MD식품, 푸드)를 건너뛰기
        if i == len(indexes) - 3:
            break
        url = index.get_attribute('href')
        category = index.text
        index_list.append({
            "url": url,
            "category": category
        })

    print(index_list)
    return index_list

def crawl_hollys():
    cafe_name = 'hollys'
    driver = setup_driver()
    
    try:
        data = []
        index_list = save_index(driver)
        for entry in index_list:
            url = entry["url"]
            category = entry["category"]
            if category == "할리치노 · 빙수":
                category = "할리치노"
            note = ''
            print(f'# 카테고리 순회 - {category}')
            driver.get(url)
            driver.implicitly_wait(3)
            try:
                button = WebDriverWait(driver, 3).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.more_menu > a')))
                driver.execute_script("arguments[0].click();", button)
            except TimeoutException:
                # 버튼이 없을 경우 그냥 넘어감
                print("More' 버튼이 없습니다.")
                pass

            # 모든 메뉴 항목을 한 번에 가져옴
            menu_items = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.menu_list01 > li"))
            )

            for item in menu_items:
                menu_name = item.find_element(By.CSS_SELECTOR, 'a').text
                image_url = item.find_element(By.CSS_SELECTOR, 'a > img').get_attribute('src')
                    
                menu_name = menu_name.replace('\n', ' ')  # \n을 공백으로 대체
                menu_name = re.sub(r'<br\s*/?>', ' ', menu_name)  # <br> 태그를 공백으로 대체
                    
                if menu_name and "빙수" not in menu_name:
                    data.append({
                            "menu_name": menu_name,
                            "image_url": image_url,
                            "category": category,
                            "note": note,
                        })
                    print(f"[{category}] {menu_name} - {note}")
                    print(image_url)

        save_data(cafe_name, data)

    finally:
        driver.quit()

if __name__ == "__main__":
    crawl_hollys()