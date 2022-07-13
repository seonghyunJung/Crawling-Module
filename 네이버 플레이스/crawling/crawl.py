from selenium.webdriver.common.by import By
import time

def naver_place_review(driver, url, hospital_kind, hospital):
    try:
        driver.get(url)
        # print('연결성공')
        result = []
        try:
            try:
                hospitalUrl = driver.find_elements(By.XPATH,
                                                   '//*[@id="loc-main-section-root"]/section/div/ul/li[contains(.,' + hospital + ')]')
            except:
                hospitalUrl = driver.find_elements(By.XPATH,
                                                   '//*[@id="loc-main-section-root"]/section/div/ul/li')
            if len(hospitalUrl) == 0:
                url = 'https://m.place.naver.com/place/list?level=top&entry=pll&x=null&y=null&query=' + hospital
                driver.get(url)
                try:
                    hospitalUrl = driver.find_element(By.XPATH,
                                                      '//*[@id="_list_scroll_container"]/div/div/div[2]/ul/li/div[2]/a[1][contains(.,' + hospital + ')]')
                except:
                    hospitalUrl = driver.find_element(By.XPATH,
                                                      '//*[@id="_list_scroll_container"]/div/div/div[2]/ul/li/div[2]/a[1]')
                reviewDtail = hospitalUrl.get_attribute('href').split('/')[-1].split('?')[0]
                reviewUrl = 'https://pcmap.place.naver.com/hospital/' + reviewDtail + '/review/visitor'
                script = f"window.open('{reviewUrl}');"
                driver.execute_script(script)
                driver.switch_to.window(driver.window_handles[-1])
                # time.sleep(3)
                moreButton = driver.find_elements(By.CSS_SELECTOR, 'div._2kAri')
                while len(moreButton) > 0:
                    moreButton[0].click()
                    time.sleep(1)
                    moreButton = driver.find_elements(By.CSS_SELECTOR, 'div._2kAri')
                try:
                    comentMoreBtn = driver.find_elements(By.CSS_SELECTOR, 'span._3_09q')
                    print(len(comentMoreBtn))
                    if len(comentMoreBtn) > 0:
                        for btn in comentMoreBtn:
                            driver.execute_script('arguments[0].click();', btn)
                            # btn.click()
                except:
                    print('없음')
                try:
                    contents = driver.find_elements(By.CSS_SELECTOR, 'li._3l2Wz')
                    for review in contents:
                        content = {
                            'review': review.find_element(By.CSS_SELECTOR, 'div.faZHB').text,
                            'date': review.find_element(By.XPATH, '//div[3]/span[1]/span[2]').text
                        }
                        result.append(content)
                except:
                    print('없음')
                # print(result)
            else:
                for i in hospitalUrl:
                    reviewDtail = i.get_attribute('data-loc_plc-doc-id')
                    reviewUrl = 'https://pcmap.place.naver.com/hospital/' + reviewDtail + '/review/visitor'
                    script = f"window.open('{reviewUrl}');"
                    driver.execute_script(script)
                    driver.switch_to.window(driver.window_handles[1])
                    # time.sleep(3)
                    moreButton = driver.find_elements(By.CSS_SELECTOR, 'div._2kAri')
                    while len(moreButton) > 0:
                        moreButton[0].click()
                        time.sleep(1)
                        moreButton = driver.find_elements(By.CSS_SELECTOR, 'div._2kAri')
                    try:
                        comentMoreBtn = driver.find_elements(By.CSS_SELECTOR, 'span._3_09q')
                        print(len(comentMoreBtn))
                        if len(comentMoreBtn) > 0:
                            for btn in comentMoreBtn:
                                driver.execute_script('arguments[0].click();', btn)
                                # btn.click()
                    except:
                        print('없음')
                    try:
                        contents = driver.find_elements(By.CSS_SELECTOR, 'li._3l2Wz')
                        for review in contents:
                            content = {
                                'review': review.find_element(By.CSS_SELECTOR, 'div.faZHB').text,
                                'date': review.find_element(By.XPATH, '//div[3]/span[1]/span[2]').text
                            }
                            result.append(content)
                    except:
                        print('없음')
                    print(result)
                    break
            return result
        except Exception as e:
            print('tistory Error:', e)
            result = 0
            return result
    except Exception as e:
        print('사이트 오류')
        result = 0
    return result

