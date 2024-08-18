from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from crawler import *
import time

def crawl_baskin():
    cafe_name = 'baskin'
    base_url = "https://www.baskinrobbins.co.kr/menu/list.php?category="

    driver = setup_driver()

    try:
        data = []
        categories = ['A', 'F', 'B', 'E', '5', '6', '7', '8']

        for category in categories :
            url = base_url + category
            driver.get(url)
            driver.implicitly_wait(3)

            menu_items = driver.find_elements(By.CSS_SELECTOR, "div.menu_list > ul > li")
            for item in menu_items:
                try:
                    menu_name = item.find_element(By.CSS_SELECTOR, 'p.tit').text
                    print(menu_name)
                    image_url = item.find_element(By.TAG_NAME, 'img').get_attribute('src')
                    print(image_url)

                    data.append({
                        "menu_name": menu_name,
                        "image_url": image_url,
                    })

                except Exception as e:
                    print(f"Error processing menu item: {str(e)}")

            save_data(cafe_name, data)
    finally:
        driver.quit()

if __name__ == "__main__":
    crawl_theventi()
