import pandas as pd
import re

# 엑셀 파일 리뷰 부분 전처리하는 함수(.xlsx 제외하고 입력)
def do_preprocess(file_name):
    df = pd.read_excel(file_name + ".xlsx")
    not_using_text_list = ["한줄평", "병원리뷰", r"[0-9]."]
    
    df.drop('Unnamed: 0',axis=1,inplace=True)

    for i in range(len(df)):
        temp = df.loc[i, '리뷰']
        temp = preprocess(temp)
        
        for not_using_text in not_using_text_list:
            temp = remove_text(temp, not_using_text)
            
        df.loc[i, '리뷰'] = temp

    df.to_excel(file_name + "전처리" + ".xlsx")

    
# 텍스트 전처리하는 함수
def preprocess(text):
    text= re.sub(r"[ㄱ-ㅎㅏ-ㅣ]+", ".", text)
    text = re.sub(r"[\`\~\@\#\$\%\^\&\*\(\)\-\_\=\+\<\>\;\:\'\"\[\]\{\}\\\/]", " ", text)
    text = re.sub(r"[^가-힣A-Za-z0-9\.\?\!]", " ", text)
    text = re.sub(r"\s*[\.]+", ".", text)
    text = re.sub(r"\s*[\?]+", "?", text)
    text = re.sub(r"\s*[\!]+", "!", text)
    text = re.sub(r"\s+", " ", text)
    text.strip()
    
    return text


# 불용어 제거하는 함수
def remove_text(original_text, not_using_text):
    result = re.sub(not_using_text, "", original_text)
    
    return result