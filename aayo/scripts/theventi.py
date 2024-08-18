from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from crawler import *
import time

def crawl_theventi():
    cafe_name = 'theventi'
    base_url = "https://www.theventi.co.kr/new2022/menu/all.html?mode="

    driver = setup_driver()

    try:
        data = []
        categories_num = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

        # 먼저 모든 카테고리 이름을 가져옵니다.
        driver.get(base_url + '1')
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.tabwrap > ul > li"))
        )
        category_elements = driver.find_elements(By.CSS_SELECTOR, "div.tabwrap > ul > li")
        category_names = [element.text.strip() for element in category_elements if element.text.strip()]

        for index, category_num in enumerate(categories_num):
            url = base_url + category_num
            driver.get(url)

            try:
                # Wait for the menu items to be visible
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.menu_list > ul > li"))
                )

                # Use the pre-fetched category name
                category = category_names[index] if index < len(category_names) else f"Category {category_num}"

                # Get menu items
                menu_items = driver.find_elements(By.CSS_SELECTOR, "div.menu_list > ul > li")

                for item in menu_items:
                    try:
                        menu_name = item.find_element(By.CLASS_NAME, 'tit').text
                        image_url = item.find_element(By.TAG_NAME, 'img').get_attribute('src')
                        note = ''

                        if menu_name:
                            data.append({
                                "menu_name": menu_name,
                                "image_url": image_url,
                                "category": category,
                                "note": note,
                            })
                            print(f"[{category}] {menu_name} - {note}")
                            print(image_url)
                    except Exception as e:
                        print(f"Error processing menu item: {e}")

            except TimeoutException:
                print(f"Timeout while loading page for category {category_num}")

        save_data(cafe_name, data)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    crawl_theventi()