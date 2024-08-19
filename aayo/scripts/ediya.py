from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException
from crawler import *
import time
import random

def wait_and_click(driver, selector, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
        )
        driver.execute_script("arguments[0].click();", element)
        time.sleep(random.uniform(1, 2))  # 랜덤 대기 시간
        return True
    except (TimeoutException, NoSuchElementException):
        return False

def click_more_buttons(driver):
    while True:
        try:
            if not wait_and_click(driver, "div.block_hot > div > div > a"):
                break
        except Exception as e:
            print(f"더보기 버튼 클릭 중 오류 발생: {e}")
            break

def get_element_info(driver, item):
    try:
        script = """
        var item = arguments[0];
        var menuName = item.querySelector('div.menu_tt > a > span').textContent;
        var imageUrl = item.querySelector('#menu_ul > li > a > img').src;
        var note = item.querySelector('.pro_detail .detail_txt p').textContent;
        return [menuName, imageUrl, note];
        """
        return driver.execute_script(script, item)
    except Exception as e:
        print(f"요소 정보 추출 중 오류 발생: {e}")
        return "", "", ""

def process_category(driver, category_index):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # 1. 카테고리 선택
            categories = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#blockcate > div > div > ul > li"))
            )
            category = categories[category_index]
            category_name = category.find_element(By.CSS_SELECTOR, 'label').text
            print(f"현재 카테고리: {category_name}")
            wait_and_click(driver, f"#blockcate > div > div > ul > li:nth-child({category_index+1}) > label")
            time.sleep(random.uniform(2, 3))

            # 2. 더보기 버튼 클릭
            click_more_buttons(driver)

            # 3. 크롤링
            menu_items = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#menu_ul > li"))
            )
            
            category_data = []
            for item in menu_items:
                menu_name, image_url, note = get_element_info(driver, item)
                
                print(f"카테고리: {category_name}")
                print(f"메뉴명: {menu_name}")
                print(f"이미지 URL: {image_url}")
                print(f"기타 설명: {note}")

                category_data.append({
                    "category": category_name,
                    "menu_name": menu_name,
                    "image_url": image_url,
                    "note": note,
                })

            # 4. 카테고리 버튼 재선택 (비활성화)
            wait_and_click(driver, f"#blockcate > div > div > ul > li:nth-child({category_index+1}) > label")
            time.sleep(random.uniform(1, 2))

            return category_data

        except StaleElementReferenceException:
            if attempt < max_retries - 1:
                print(f"Stale element encountered. Retrying... (Attempt {attempt + 1})")
                driver.refresh()
                time.sleep(random.uniform(3, 5))
            else:
                print(f"Failed to process category after {max_retries} attempts.")
                return []

        except Exception as e:
            print(f"카테고리 처리 중 오류 발생: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying... (Attempt {attempt + 1})")
                driver.refresh()
                time.sleep(random.uniform(3, 5))
            else:
                print(f"Failed to process category after {max_retries} attempts.")
                return []

def crawl_ediya():
    cafe_name = 'ediya'
    url = "https://ediya.com/contents/drink.html#c"
    driver = setup_driver()

    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#blockcate > div > div > ul > li"))
        )

        data = []
        category_count = len(driver.find_elements(By.CSS_SELECTOR, "#blockcate > div > div > ul > li"))
        
        for i in range(category_count):
            category_data = process_category(driver, i)
            data.extend(category_data)

        save_data(cafe_name, data)
        print(f"총 {len(data)}개의 메뉴 항목을 크롤링했습니다.")

    except Exception as e:
        print(f"크롤링 중 오류 발생: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    crawl_ediya()
    