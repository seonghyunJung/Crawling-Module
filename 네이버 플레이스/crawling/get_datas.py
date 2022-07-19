from crawl import *
import pandas as pd
from tqdm import tqdm
import xlsxwriter


def get_data(driver, hospital_kind, hospital_list):
    # 데이터 프레임 생성 및 데이터 입력
    df = pd.DataFrame(columns = ['분과', '병원명', '리뷰', '날짜'])
    total = 0
    for hospital in tqdm(hospital_list[hospital_kind]):
        if (total > 25000):
                break
        try:
            data = naver_place_crawl(driver, hospital)
            num = len(data)
            

            for i in tqdm(range(num)):
                df.loc[total] = [hospital_kind, hospital, data[i].get('review'), data[i].get('date')]
                total += 1

            print(f'총 리뷰 갯수 : {total}')
        
        except Exception as e:
            print(e)
            pass


    df.to_excel(f'크롤링 결과/네이버({hospital_kind}).xlsx', sheet_name = hospital_kind, engine='xlsxwriter')
