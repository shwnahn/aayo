from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from crawler import *
import time

def crawl_coffeebean():
    cafe_name = 'coffeebean'
    base_url = "https://www.coffeebeankorea.com/menu/list.asp?category="

    driver = setup_driver()

    try:
        data = []
        categories = ['11', '12', '13', '14', '17', '18', '24', '26']

        for category in categories :
            url = base_url + category
            driver.get(url)
            driver.implicitly_wait(3)

            menu_items = driver.find_elements(By.CSS_SELECTOR, ".menu_list > ul > li")

        
            for item in menu_items:
                try:
                    menu_name = item.find_element(By.CLASS_NAME, 'kor').text
                    image_url = item.find_element(By.TAG_NAME, 'img').get_attribute('src')
                    
                    print(menu_name, image_url)

                    data.append({
                        "menu_name": menu_name,
                        "image_url": image_url,
                    })

                except Exception as e:
                    print(f"Error processing menu item: {str(e)}")
                    
                # try:
                #     next_button = driver.find_element(By.CSS_SELECTOR, "div.paging > a.next")
                #     if 'disabled' in next_button.get_attribute('class'):
                #         break
                #     next_button.click()
                #     time.sleep(2)
                # except Exception as e:
                #     print(f"No more pages or error navigating: {str(e)}")
                #     break
        
        save_data(cafe_name, data)
    finally:
        driver.quit()

if __name__ == "__main__":
    crawl_coffeebean()