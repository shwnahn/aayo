from selenium.webdriver.common.by import By
from crawler import *
import time

def crawl_paik(driver, url, is_new_menu=False):
    data = []

    try:
        driver.get(url)
        driver.implicitly_wait(5)  # 5초 동안 대기

        if is_new_menu:
            menu_items = driver.find_elements(By.CSS_SELECTOR, "div.swiper-slide.swiper-slide-active, div.swiper-slide.swiper-slide-next")
            name_selector = 'p.best_tit'
            image_selector = 'img'
        else:
            menu_items = driver.find_elements(By.CSS_SELECTOR, "div.menu_list.clear > ul > li")
            name_selector = 'p.menu_tit'
            image_selector = 'div.thumb > img'

        for item in menu_items:
            try:
                menu_name = item.find_element(By.CSS_SELECTOR, name_selector).text
                image_url = item.find_element(By.CSS_SELECTOR, image_selector).get_attribute('src')
                
                print(f"메뉴명: {menu_name}, 이미지 URL: {image_url}")

                data.append({
                    "menu_name": menu_name,
                    "image_url": image_url,
                })
            except Exception as e:
                print(f"메뉴 항목 처리 중 오류 발생: {e}")

    except Exception as e:
        print(f"크롤링 중 오류 발생: {e}")

    return data

def main():
    cafe_name = 'paik'
    all_data = []

    urls = [
        "https://paik.com/menu/menu_new/",
        "https://paik.com/menu/menu_coffee/",
        "https://paik.com/menu/menu_drink/",
        "https://paik.com/menu/menu_ccino/"
    ]

    driver = setup_driver()

    try:
        for url in urls:
            is_new_menu = 'menu_new' in url
            data = crawl_paik(driver, url, is_new_menu)
            all_data.extend(data)
            time.sleep(2) # 웹사이트 부하 방지

        save_data(cafe_name, all_data)

    except Exception as e:
        print(f"전체 크롤링 과정 중 오류 발생: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()