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

            while True:



            # menu_items = driver.find_elements(By.CSS_SELECTOR, "ul.menu_list > li")
            # next_button = driver.find_element(By.CSS_SELECTOR, "div.paging > a.next")
            # children = driver.find_elements(By.CSS_SELECTOR, 'div.paging > a')
            # pages = driver.find_elements(By.CSS_SELECTOR, "div.paging")
            # first_child = children[0]
            # last_child = children[-1]
            # # print(children)

            # if 'on' in first_child.get_attribute('class'):
            #     for item in menu_items:
            #         try:
            #             menu_name = item.find_element(By.CLASS_NAME, 'kor').text
            #             image_url = item.find_element(By.TAG_NAME, 'img').get_attribute('src')
                        
            #             print(menu_name, image_url)

            #             data.append({
            #                 "menu_name": menu_name,
            #                 "image_url": image_url,
            #             })

            #         except Exception as e:
            #             print(f"Error processing menu item: {str(e)}")
            # else:
                
            #     for page in page_numbers:
            #         for item in menu_items:
            #             if 'on' not in last_child.get_attribute('class'):
            #                 try:
            #                     menu_name = item.find_element(By.CLASS_NAME, 'kor').text
            #                     image_url = item.find_element(By.TAG_NAME, 'img').get_attribute('src')
                                
            #                     print(menu_name, image_url)

            #                     data.append({
            #                         "menu_name": menu_name,
            #                         "image_url": image_url,
            #                     })

            #                 except Exception as e:
            #                     print(f"Error processing menu item: {str(e)}")
            #             try:
            #                 next_button.click()
            #                 time.sleep(2)
            #             except Exception as e:
            #                 print(f"No more pages or error navigating: {str(e)}")
            #                 break
            #             else:
            #                 try:
            #                     menu_name = item.find_element(By.CLASS_NAME, 'kor').text
            #                     image_url = item.find_element(By.TAG_NAME, 'img').get_attribute('src')
                                
            #                     print(menu_name, image_url)

            #                     data.append({
            #                         "menu_name": menu_name,
            #                         "image_url": image_url,
            #                     })

            #                 except Exception as e:
            #                     print(f"Error processing menu item: {str(e)}")

            




                # for item in menu_items:
                #     try:
                #         menu_name = item.find_element(By.CLASS_NAME, 'kor').text
                #         image_url = item.find_element(By.TAG_NAME, 'img').get_attribute('src')
                        
                #         print(menu_name, image_url)

                #         data.append({
                #             "menu_name": menu_name,
                #             "image_url": image_url,
                #         })

                #     except Exception as e:
                #         print(f"Error processing menu item: {str(e)}")
                # try:
                #     next_button.click()
                #     time.sleep(2)
                # except Exception as e:
                #     print(f"No more pages or error navigating: {str(e)}")
                #     break

            # while 'disabled' not in next_button:
            #     for item in menu_items:
            #         try:
            #             menu_name = item.find_element(By.CLASS_NAME, 'kor').text
            #             image_url = item.find_element(By.TAG_NAME, 'img').get_attribute('src')
                        
            #             print(menu_name, image_url)

            #             data.append({
            #                 "menu_name": menu_name,
            #                 "image_url": image_url,
            #             })

            #         except Exception as e:
            #             print(f"Error processing menu item: {str(e)}")
                    
            #     try:
            #         next_button.click()
            #         time.sleep(2)
            #     except Exception as e:
            #         print(f"No more pages or error navigating: {str(e)}")
            #         break
        
        # save_data(cafe_name, data)
    finally:
        driver.quit()

if __name__ == "__main__":
    crawl_coffeebean()