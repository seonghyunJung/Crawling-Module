import config
import web
import logger
import time
from crawl import *
import re
import pandas as pd

# Globals
logger = logger.instance


def main():
    logger.info('Script started.')
    config.init_web()

    web.start()
    driver = web.driver
    driver.get('https://www.google.com')
    time.sleep(2)

    url = "https://map.naver.com/v5/search/%ED%94%BC%EB%B6%80%EA%B3%BC"
    hospital = "차앤유의원"
    hospital_kind = "피부과"

    data = naver_place_review(driver, url, hospital_kind, hospital)
    print(data)

    # 데이터 프레임 생성 및 데이터 입력
    df = pd.DataFrame(columns = ['분과', '병원명', '리뷰', '날짜'])
    num = len(data)

    for i in range(num):
        df.loc[i] = [hospital_kind, hospital, data[i].get('review'), data[i].get('date')]

    df.to_excel("test.xlsx", sheet_name = hospital_kind)

if __name__ == '__main__':
    main()
