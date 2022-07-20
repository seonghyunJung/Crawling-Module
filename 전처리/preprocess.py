import pandas as pd
import re

# 엑셀 파일 리뷰 부분 전처리하는 함수(.xlsx 제외하고 입력)
def do_preprocess(file_name):
    df = pd.read_excel(file_name + ".xlsx")
    not_using_text_list = ["한줄평", "병원리뷰"]


    for i in range(len(df)):
        temp = df.loc[i, '리뷰']
        
        for not_using_text in not_using_text_list:
            temp = remove_text(temp, not_using_text)
        
        temp = preprocess(temp)
#         if len(temp) < 5:
#             df.drop(df.index[i], inplace = True)
        
        
        temp = change_last(temp)
        temp = add_last_point(temp)
        df.loc[i, '리뷰'] = temp
    
    # 문장 길이 5 미만 제거
    index_rows = df[df['리뷰'].map(len) < 5].index
    df.drop(index_rows, inplace = True)
    
    # 중복 문장 제거
    df.drop_duplicates(subset = ['리뷰'], inplace = True, keep = 'first', ignore_index=True)
    df.drop('Unnamed: 0',axis=1,inplace=True)
    df.to_excel(file_name + "전처리" + ".xlsx")

    
# 텍스트 전처리하는 함수
def preprocess(text):
    text= re.sub(r"[ㄱ-ㅎㅏ-ㅣ]+", " ", text)
    text = re.sub(r"[\`\~\@\#\$\%\^\&\*\(\)\-\_\=\+\<\>\;\:\'\"\[\]\{\}\\\/]", " ", text)
    text = re.sub(r"[^가-힣A-Za-z0-9\.\?\!\,]", " ", text)
    text = re.sub(r"\s*[\.]+", ".", text)
    text = re.sub(r"\s*[\?]+", "?", text)
    text = re.sub(r"\s*[\!]+", "!", text)
    text = re.sub(r"[\.\?\!\~\,]{2,}", ". ", text)       # 이모티콘 혹은 ?! 과 같이 다른 특수문자가 이어서 사용된 경우 제거
    text = re.sub(r"[\.\?\!\~\,] [\.\?\!\~\,]", ". ", text)       # 이모티콘 혹은 ?! 과 같이 다른 특수문자가 이어서 사용된 경우 제거

    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    
    return text


# 불용어 제거하는 함수
def remove_text(original_text, not_using_text):
    result = re.sub(not_using_text, "", original_text)
    
    return result

# 종결어미 표준어로 바꿔주는 함수
def change_last(text):
#     slang_last_word = ["어용", "아용", "에용", "나용", "니당", "예용", "는당", "게용", "는뎅", "구용", "네용", "세용", "해용", "가봐용", "어욥", "께용", "워용"]
    text = text.replace('어용', '어요')
    text = text.replace('어여', '어요')
    text = text.replace('아용', '아요')
    text = text.replace('아여', '아요')
    text = text.replace('에용', '에요')
    text = text.replace('에영', '에요')
    text = text.replace('에여', '에요')
    text = text.replace('나용', '나요')
    text = text.replace('니당', '니다')
    text = text.replace('예용', '예요')
    text = text.replace('는당', '는다')
    text = text.replace('게용', '게요')
    text = text.replace('게여', '게요')
    text = text.replace('게영', '게요')
    text = text.replace('는뎅', '는데')
    text = text.replace('구용', '구요')
    text = text.replace('네용', '네요')
    text = text.replace('세영', '세요')
    text = text.replace('세여', '세요')
    text = text.replace('세용', '세요')
    text = text.replace('해용', '해요')
    text = text.replace('가봐용', '가봐요')
    text = text.replace('어욥', '어요')
    text = text.replace('께용', '께요')
    text = text.replace('워용', '워요')
    text = text.replace('겨용', '겨요')
    text = text.replace('슴니다', '습니다')
    text = text.replace('쵝오', '최고')
    text = text.replace('네여', '네요')
    text = text.replace('오요', '어요')
    text = text.replace('녀용', '녀요')
    text = text.replace('녀여', '녀요')
    text = text.replace('니더', '니다')
    text = text.replace('조아요', '좋아요')
    text = text.replace('조아여', '좋아요')
    text = text.replace('조아영', '좋아요')
    text = text.replace('조아용', '좋아요')
    text = text.replace('구여', '구요')
    text = text.replace('구영', '구요')
    text = text.replace('구용', '구요')
    text = text.replace('셔여', '셔요')
    text = text.replace('셔영', '셔요')
    text = text.replace('셔용', '셔요')
    
    return text
    

# 종결어미 뒤에 마침표 붙여주는 함수
def add_last_point(text):
    words = text.split()
    # 종결어미 리스트
    last_word_list = ["나요", "아요", "어요", "니다", "에요", "예요", "는다", "게요", "구요", "네요", "구요", "세요", "해요", "가봐요", "께요", "워요", "래요", "겨요", "하셔요", "라요", "려고요", "녀요", "줘요", "려요", "되요", "돼요", "구요", "셔요"]
    last_points = ['!', '.', ',', '?']
    for i in range(len(words)):
        for last_word in last_word_list:
            index = words[i].find(last_word)
            if index != -1:
                if words[i][-1] not in last_points:
                    words[i] = words[i] + '.'

    text = ' '.join(words)
    
    return text





# # 엑셀 파일 리뷰 부분 전처리하는 함수(.xlsx 제외하고 입력)
# def do_preprocess(file_name):
#     df = pd.read_excel(file_name + ".xlsx")
#     not_using_text_list = ["한줄평", "병원리뷰", r"[0-9]."]
    
#     df.drop('Unnamed: 0',axis=1,inplace=True)

#     for i in range(len(df)):
#         temp = df.loc[i, '리뷰']
#         temp = preprocess(temp)
        
#         for not_using_text in not_using_text_list:
#             temp = remove_text(temp, not_using_text)
            
#         df.loc[i, '리뷰'] = temp

#     df.to_excel(file_name + "전처리" + ".xlsx")

    
# # 텍스트 전처리하는 함수
# def preprocess(text):
#     text= re.sub(r"[ㄱ-ㅎㅏ-ㅣ]+", ".", text)
#     text = re.sub(r"[\`\~\@\#\$\%\^\&\*\(\)\-\_\=\+\<\>\;\:\'\"\[\]\{\}\\\/]", " ", text)
#     text = re.sub(r"[^가-힣A-Za-z0-9\.\?\!]", " ", text)
#     text = re.sub(r"\s*[\.]+", ".", text)
#     text = re.sub(r"\s*[\?]+", "?", text)
#     text = re.sub(r"\s*[\!]+", "!", text)
#     text = re.sub(r"\s+", " ", text)
#     text.strip()
    
#     return text


# # 불용어 제거하는 함수
# def remove_text(original_text, not_using_text):
#     result = re.sub(not_using_text, "", original_text)
    
#     return result


# # 최종 전처리하는 함수(글자 수, 중복 문장)
# def do_preprocess_last(file_name):
#     df = pd.read_excel(file_name + ".xlsx")

#       # 중복 문장 제거
#     df.drop_duplicates(subset = ['리뷰'], inplace = True, keep = 'first', ignore_index=True)

#     for i in range(len(df)):
#         temp = df.loc[i, '리뷰']
#         if len(temp) < 10:
#             df.drop(df.index[i])
            
        
#     df.drop('Unnamed: 0',axis=1,inplace=True)
#     df.to_excel(file_name + "전처리(최종)" + ".xlsx")
