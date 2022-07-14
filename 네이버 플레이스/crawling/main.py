import config
import web
import logger
import time
from crawl import *
import re
import pandas as pd
from get_hospitals import get_hospital_list
from tqdm import tqdm


# Globals
logger = logger.instance


def main():
    logger.info('Script started.')
    config.init_web()

    

    web.start()
    driver = web.driver
    driver.get('https://www.google.com')
    time.sleep(1)

    # 병원 분과 종류
    hospital_kind_list = ['치과', '피부과', '성형외과', '산부인과', '정신건강의학과', '비뇨기과','재활의학과', '외과', '소아과', '가정의학과', '한의원']

    # hospital_kind_list = ['한의원']
    hospital_list = {}
    
    for hospital_kind in hospital_kind_list:
        hospital_list[hospital_kind] = get_hospital_list(driver, hospital_kind)


    for hospital_kind in hospital_kind_list:


        # 데이터 프레임 생성 및 데이터 입력
        df = pd.DataFrame(columns = ['분과', '병원명', '리뷰', '날짜'])
        total = 0
        for hospital in tqdm(hospital_list[hospital_kind]):
            if (total > 25000):
                break
            data = naver_place_review(driver, hospital)
            num = len(data)
            

            for i in tqdm(range(num)):
                df.loc[total] = [hospital_kind, hospital, data[i].get('review'), data[i].get('date')]
                total += 1

        df.to_excel(f'크롤링 결과/네이버({hospital_kind}).xlsx', sheet_name = hospital_kind)

        
   

    # hospital_kind = '한의원'
    # # 데이터 프레임 생성 및 데이터 입력
    # df = pd.DataFrame(columns = ['분과', '병원명', '리뷰', '날짜'])
    # hospital = '신곡경희한의원'
    # data = naver_place_review(driver, hospital)
    # # print(data)
    
    # num = len(data)

    # for i in range(num):
    #     df.loc[i] = [hospital_kind, hospital, data[i].get('review'), data[i].get('date')]

    # df.to_excel(writer, sheet_name = hospital_kind)
    # writer.save()

if __name__ == '__main__':
    main()
