from selenium.webdriver.common.by import By
from crawler import * 
import time 

def crawl_bana():
    cafe_name = 'bana'
    url = "https://www.banapresso.com/menu"

    driver = setup_driver()

    try:
        driver.get(url)
        driver.implicitly_wait(3)

        data = []
        menu_items = driver.find_elements(By.CLASS_NAME, "menu_box")
        
        for item in menu_items:
            menu_name = item.find_element(By.CSS_SELECTOR, 'div > em > div > i').text
            image_url = item.find_element(By.TAG_NAME, 'img').get_attribute('data-src')
            
            print(menu_name, image_url) 

            data.append({
                "menu_name": menu_name,
                "image_url": image_url,
            })
        
        save_data(cafe_name, data)
    finally:
        driver.quit()

if __name__ == "__main__":
    crawl_bana()