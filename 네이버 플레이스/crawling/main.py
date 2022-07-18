import config
import web
import logger
import time
from crawl import *
import re
import pandas as pd
from get_hospitals import get_hospital_list
from get_datas import *
from tqdm import tqdm
import threading
import multiprocessing


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
    hospital_kind_list = ['치과', '피부과', '성형외과', '산부인과', '정신건강의학과', '비뇨기과','재활의학과', '외과', '소아과', '가정의학과', '한의원', '요양병원']

    # hospital_kind_list = ['가정의학과']
    # hospital_list = {}
    
    # for hospital_kind in hospital_kind_list:
    #     hospital_list[hospital_kind] = get_hospital_list(driver, hospital_kind)


    # threads = []
    # pool = multiprocessing.Pool(processes=3)


    for hospital_kind in hospital_kind_list:
        hospital_list = {}
        hospital_list[hospital_kind] = get_hospital_list(driver, hospital_kind)
        get_data(driver, hospital_kind, hospital_list)

        
        # t = threading.Thread(target=get_data(driver, hospital_kind, hospital_list))
        # threads.append(t)

        # # 데이터 프레임 생성 및 데이터 입력
        # df = pd.DataFrame(columns = ['분과', '병원명', '리뷰', '날짜'])
        # total = 0
        # for hospital in tqdm(hospital_list[hospital_kind]):
        #     try:
        #         if (total > 1000):
        #             break
        #         data = naver_place_review(driver, hospital)
        #         num = len(data)
                

        #         for i in tqdm(range(num)):
        #             df.loc[total] = [hospital_kind, hospital, data[i].get('review'), data[i].get('date')]
        #             total += 1
            
        #     except Exception as e:
        #         print(e)
        #         pass


        # df.to_excel(f'크롤링 결과/네이버({hospital_kind}).xlsx', sheet_name = hospital_kind)

    # for thread in threads:
    #     thread.start()
    #     thread.join()


if __name__ == '__main__':
    start = time.time()  # 시작 시간 저장
    main()
    print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간
