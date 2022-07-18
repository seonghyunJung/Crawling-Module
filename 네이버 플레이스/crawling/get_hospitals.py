import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import web

# 현재 페이지 내 모든 병원 리스트에 저장하는 함수
def get_hospital_list(driver, hospital_kind):
    web.start()
    driver = web.driver
    try:
        url = "https://m.place.naver.com/place/list?level=top&entry=pll&x=null&y=null&query=" + hospital_kind
        driver.get(url)
        do_scroll(driver)

        data = []

        elements  = driver.find_elements(By.CLASS_NAME, "place_bluelink")

        for element in elements:
            data.append(element.text)
    finally:
        driver.quit()

    return data


# 스크롤 끝까지 내리는 함수
def do_scroll(driver):
    # Click on element inside the main content to switch focus
    driver.find_element(By.XPATH, '//div[@class="_2YHxL"]').click()

    for i in range(30):
        # Scroll page down
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(1)


