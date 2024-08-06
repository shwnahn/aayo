from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from crawler import *  # setup_driver, save_data 불러옴
import time  # time.sleep 쓰려고

def crawl_hollys(driver, url):
    data = []

    try:
        crawled_items = set()
        driver.get(url)
        driver.implicitly_wait(5)  # 5초 동안 대기
        
        menu_items = driver.find_elements(By.CSS_SELECTOR, "ul.menu_list.line > li")

        for item in menu_items:
            print()
            menu_name = item.find_element(By.CSS_SELECTOR, 'ul.menu_list.line > li > a > span.name').text
            image_url = item.find_element(By.CSS_SELECTOR, 'ul.menu_list.line > li > a > span.img > img').get_attribute('src')
                
            if (menu_name, image_url) not in crawled_items:
                if '빙수' in menu_name:  # 빙수 메뉴는 제외
                    continue
                data.append({'menu_name': menu_name, 'image_url': image_url})
                crawled_items.add((menu_name, image_url))
                print(f"URL: {url}, Menu: {menu_name}, Image: {image_url}")
            try:
                more_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/section[5]/div[2]/button'))
                )
                driver.execute_script("arguments[0].click();", more_button)
                time.sleep(1)  
            except TimeoutException:
                print("더 이상 '더보기' 버튼이 없습니다.")
                break
    except Exception as e:
        print(f"크롤링 중 오류 발생: {e}")

    return data

def main():
    cafe_name = 'hollys'
    all_data = []

    urls = [
        "https://www.hollys.co.kr/menu/espresso.do",
        "https://www.hollys.co.kr/menu/signature.do",
        "https://www.hollys.co.kr/menu/hollyccino.do",
        "https://www.hollys.co.kr/menu/juice.do",
        "https://www.hollys.co.kr/menu/tea.do"
    ]

    driver = setup_driver()

    try:
        for url in urls:
            data = crawl_hollys(driver, url)
            all_data.extend(data)
            time.sleep(2) # 웹사이트 부하 방지

        #save_data(cafe_name, all_data)

    except Exception as e:
        print(f"전체 크롤링 과정 중 오류 발생: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()