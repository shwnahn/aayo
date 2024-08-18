from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from crawler import *
import time

def crawl_compose():
    cafe_name = 'compose'
    base_url = "https://composecoffee.com/menu"
    driver = setup_driver()

    try:
        driver.get(base_url)
        driver.implicitly_wait(3)

        data = []
        
        # 카테고리 목록 가져오기
        categories = driver.find_elements(By.CSS_SELECTOR, "#bd_152_0 > ul > li")
        category_count = len(categories)

        for i in range(category_count):
            try:
                # 카테고리 목록을 매번 새로 가져옴
                categories = driver.find_elements(By.CSS_SELECTOR, "#bd_152_0 > ul > li")
                category = categories[i]
                category_name = category.text
                
                # 제외할 카테고리 목록
                excluded_categories = ['전체', '디저트', 'MD상품', '']
                if category_name in excluded_categories:
                    continue

                print(f"카테고리 '{category_name}' 크롤링 중...")
                
                # 카테고리 클릭 (여러 방법 시도)
                try:
                    # 방법 1: 일반 클릭
                    category.click()
                except (ElementClickInterceptedException, StaleElementReferenceException):
                    try:
                        # 방법 2: JavaScript로 클릭
                        driver.execute_script("arguments[0].click();", category)
                    except:
                        try:
                            # 방법 3: ActionChains 사용
                            from selenium.webdriver.common.action_chains import ActionChains
                            ActionChains(driver).move_to_element(category).click().perform()
                        except:
                            print(f"카테고리 '{category_name}' 클릭 실패")
                            continue

                time.sleep(2)  # 카테고리 로딩 대기
                
                # 현재 URL 가져오기
                current_url = driver.current_url
                
                # 페이지 버튼 수 계산
                page_buttons = driver.find_elements(By.CSS_SELECTOR, "#bd_152_0 > nav > ul > li:not(.prev):not(.next)")
                total_pages = len(page_buttons) - 2
                
                print(f"총 {total_pages}개의 페이지가 있습니다.")

                for page_number in range(1, total_pages + 1):
                    print(f"페이지 {page_number}/{total_pages} 크롤링 중...")
                    
                    # URL을 통해 페이지 이동
                    page_url = f"{current_url}?page={page_number}"
                    driver.get(page_url)
                    time.sleep(2)  # 페이지 로딩 대기

                    # 현재 페이지의 메뉴 목록이 표시될 때까지 대기
                    try:
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "#masonry-container > div"))
                        )
                    except TimeoutException:
                        print(f"페이지 {page_number} 메뉴 로딩 실패")
                        continue

                    # 현재 페이지의 메뉴 아이템 찾기
                    menu_items = driver.find_elements(By.CSS_SELECTOR, "#masonry-container > div")
                    
                    for item in menu_items:
                        try:
                            menu_name = item.find_element(By.CSS_SELECTOR, 'h3').text
                            image_url = item.find_element(By.CSS_SELECTOR, '#rthumbnail > img').get_attribute('src')
                            
                            print(f"카테고리: {category_name}, 메뉴명: {menu_name}, 이미지 URL: {image_url}")

                            data.append({
                                "category": category_name,
                                "menu_name": menu_name,
                                "image_url": image_url,
                            })
                        except (NoSuchElementException, StaleElementReferenceException) as e:
                            print(f"메뉴 항목 처리 중 오류 발생: {e}")

            except Exception as e:
                print(f"카테고리 처리 중 오류 발생: {e}")
                continue

        # JSON 파일로 저장
        save_data(cafe_name, data)
        print(f"총 {len(data)}개의 메뉴 항목을 크롤링했습니다.")

    except Exception as e:
        print(f"크롤링 중 오류 발생: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    crawl_compose()