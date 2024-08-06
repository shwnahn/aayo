from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from crawler import *
import time

def click_more_button(driver):
    while True:
        try:
            more_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.block_hot > div > div > a"))
            )
            driver.execute_script("arguments[0].click();", more_button)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)
        except TimeoutException:
            print("더 이상 '더보기' 버튼이 없습니다.")
            break

def crawl_ediya():
    cafe_name = 'ediya'
    url = "https://ediya.com/contents/drink.html#c"
    driver = setup_driver()

    try:
        driver.get(url)
        driver.implicitly_wait(3)

        # 일단 더보기 버튼 싹 다 눌러서 모든 메뉴 띄우고 크롤링하는 로직
        click_more_button(driver)

        # 모든 메뉴 아이템을 찾습니다.
        menu_items = driver.find_elements(By.CSS_SELECTOR, "#menu_ul > li")
        
        data = []
        for item in menu_items:
            try:
                menu_name = item.find_element(By.CSS_SELECTOR, 'div.menu_tt > a > span').text
                image_url = item.find_element(By.CSS_SELECTOR, 'a:nth-child(2) > img').get_attribute('src')
                
                print(f"메뉴명: {menu_name}")
                print(f"이미지 URL: {image_url}")

                data.append({
                    "menu_name": menu_name,
                    "image_url": image_url,
                })
            except Exception as e:
                print(f"메뉴 항목 처리 중 오류 발생: {e}")

        save_data(cafe_name, data)
        # print(f"총 {len(data)}개의 메뉴 항목을 크롤링했습니다.")

    except Exception as e:
        print(f"크롤링 중 오류 발생: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    crawl_ediya()