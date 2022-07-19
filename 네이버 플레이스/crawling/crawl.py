from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import web

def naver_place_crawl(driver, hospital):
    web.start()
    driver = web.driver
    try:
        url = 'https://m.place.naver.com/place/list?level=top&entry=pll&x=null&y=null&query=' + hospital
        driver. get(url)
        time.sleep(1)
        
        hospitalUrl = driver.find_element(By.CLASS_NAME, '_3LMxZ')
        hospitalCode = hospitalUrl.get_attribute('href').split('/')[-1].split('?')[0]
        reviewUrl = 'https://pcmap.place.naver.com/hospital/' + hospitalCode + '/review/visitor'
        driver.get(reviewUrl)
        time.sleep(1)
        
        try:
            while True:
                moreButton = driver.find_element(By.CLASS_NAME, '_2kAri')
                moreButton.click()
                time.sleep(1)
        except:
            print('페이지 스크롤 끝')
            pass

        try:
            commentMoreBtn = driver.find_elements(By.CLASS_NAME, '_3_09q')
            for btn in commentMoreBtn:
                driver.execute_script('arguments[0].click();', btn)
                # btn.click()
        except:
            print('더보기 없음')
            pass
        
        
        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')

        result = []
        try:
            contents = soup.select("li._3l2Wz")

            for content in contents:
                try:
                    review = content.select_one('span.WoYOw').text

                    if len(review) < 10:
                        continue

                    date = content.select_one("div._29Yga").select("span.place_blind")[1].text

                    if date == "최근 방문일":
                        date = content.select_one("div._29Yga").select("span.place_blind")[2].text
                        
                    # date = content.find_all('span', class_='place_blind')[0].text
                    # if date == '최근 방문일':
                    #     date = content.find_all('span', class_='place_blind')[1].text
                    # elif date == '별점':
                    #     date = content.find_all('span', class_='place_blind')[2].text
                    # elif date == '방문자리뷰':
                    #     date = content.find_all('span', class_='place_blind')[3].text
                    # elif date == '이전':
                    #     date = content.find_all('span', class_='place_blind')[4].text
                    # elif date == '다음':
                    #     date = content.find_all('span', class_='place_blind')[5].text

                    # if date not in '2':
                    #     continue
                        
                    data = {
                        'review': review,
                        'date': date
                    }
                    result.append(data)
                except:
                    pass
        except Exception as e:
            print(e)
    finally:
        driver.quit()
        
    return result


def naver_place_review(driver, hospital):
    try:
        # driver.get(url)
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
                # try:
                #     hospitalUrl = driver.find_element(By.XPATH,
                #                                       '//*[@id="_list_scroll_container"]/div/div/div[2]/ul/li/div[2]/a[1][contains(.,' + hospital + ')]')
                # except:
                #     hospitalUrl = driver.find_element(By.XPATH,
                #                                       '//*[@id="_list_scroll_container"]/div/div/div[2]/ul/li/div[2]/a[1]')

                hospitalUrl = driver.find_element(By.CLASS_NAME, '_3LMxZ')
                reviewDtail = hospitalUrl.get_attribute('href').split('/')[-1].split('?')[0]
                reviewUrl = 'https://pcmap.place.naver.com/hospital/' + reviewDtail + '/review/visitor'

                # script = f"window.open('{reviewUrl}');"
                # driver.execute_script(script)
                # driver.switch_to.window(driver.window_handles[-1])
                driver.get(reviewUrl)
                time.sleep(2)
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
                    # contents = driver.find_elements(By.CSS_SELECTOR, 'li._3l2Wz')
                    # for review in contents:
                    #     content = {
                    #         'review': review.find_element(By.CSS_SELECTOR, 'div.faZHB').text,
                    #         'date': review.find_element(By.XPATH, '//div[3]/span[1]/span[2]').text
                    #     }
                    #     result.append(content)
                    contents = driver.find_elements(By.CLASS_NAME, '_3l2Wz')
                    for review in contents:
                        try:
                            content = {
                                'review': review.find_element(By.CLASS_NAME, 'WoYOw').text,
                                # 'date': review.find_element(By.XPATH, '//div[3]/span[1]/span[2]').text
                                # 'date': review.find_element(By.CLASS_NAME, 'utrsf').find_elements(By.CLASS_NAME, 'place_blind')[1].text
                                'date': review.find_element(By.CLASS_NAME, '_29Yga').find_element(By.CLASS_NAME, 'utrsf').find_elements(By.CLASS_NAME, 'place_blind')[1].text
                            }
                            result.append(content)
                        except:
                            pass
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
                        # contents = driver.find_elements(By.CSS_SELECTOR, 'li._3l2Wz')
                        # for review in contents:
                        #     content = {
                        #         'review': review.find_element(By.CSS_SELECTOR, 'div.faZHB').text,
                        #         'date': review.find_element(By.XPATH, '//div[3]/span[1]/span[2]').text
                        #     }
                        #     result.append(content)
                        contents = driver.find_elements(By.CLASS_NAME, '_3l2Wz')
                        for review in contents:
                            try:
                                content = {
                                    'review': review.find_element(By.CLASS_NAME, 'WoYOw').text,
                                    # 'date': review.find_element(By.CLASS_NAME, 'utrsf').find_elements(By.CLASS_NAME, 'place_blind')[1].text
                                    'date': review.find_element(By.CLASS_NAME, '_29Yga').find_element(By.CLASS_NAME, 'utrsf').find_elements(By.CLASS_NAME, 'place_blind')[1].text
                                }
                                result.append(content)
                            except:
                                pass
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

