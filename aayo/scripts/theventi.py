from selenium.webdriver.common.by import By
from crawler import *
import time

def crawl_theventi():
    cafe_name = 'theventi'
    url = "https://www.theventi.co.kr/new2022/menu/all.html?mode="

    driver = setup_driver()

    try:
        data = []
        categories = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

        for category in categories:
            



        driver.get(url)
        driver.implicitly_wait(3)

        data = []
        menu_items = driver.find_elements(By.CLASS_NAME, "")
        
        for item in menu_items:
            menu_name = item.find_element(By.TAG_NAME, 'dd').text
            image_url = item.find_element(By.TAG_NAME, 'img').get_attribute('src')
            
            print(menu_name, image_url)

            data.append({
                "menu_name": menu_name,
                "image_url": image_url,
            })
        
        save_data(cafe_name, data)
    finally:
        driver.quit()

if __name__ == "__main__":
    crawl_theventi()