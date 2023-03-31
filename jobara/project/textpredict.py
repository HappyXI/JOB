# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 11:15:13 2023

@author: User
"""
from konlpy.tag import Okt
import pandas as pd
import pickle
import re


def text_cleaning(text):
    # 불용어 목록 
    stopwords = ['그리고', '하지만', '그런데', '따라서', '그래서', '또한', '이러한', '바로', '이런', '결국',
                 '합니다','했습니다','입니다',]

    # 한글, 영문, 숫자 및 공백만 남기고 제거
    nhangul = re.compile('[^ ㄱ-ㅣ 가-힣 a-zA-Z0-9]+')
    text = nhangul.sub("", text)
    # 텍스트를 단어로 분리
    words = text.split()
    # 불용어 제거
    cleaned_words = [word for word in words if word not in stopwords]
    # 단어를 다시 하나의 문자열로 결합
    result = ' '.join(cleaned_words)
    return result

#한글 형태소 분리 
def get_pos(text): 
    okt= Okt()
    pos=okt.pos(text)
    pos =['{0}/{1}'.format(word,t) for word, t  in pos]
    return pos

with open('model/indextocoef.pkl', 'rb') as fp:
    indextocoef = pickle.load(fp)

with open('model/texttoindex.pkl', 'rb') as fp:
    texttoindex = pickle.load(fp)

lr = pickle.load(open('model/lregression.rl', 'rb'))


df=pd.read_csv("data/cleaned_text.csv")
answer=df["답변"][60]
answer
y=df["y"][60]
y #기존 긍부정 값 확인

text = text_cleaning(answer)
text_okt=get_pos(text)
text_okt #형태소


sol=0 #분석수치
sol = 0  # 분석 수치
for tt in text_okt:
    print(tt)
    word = tt.split("/")   
    if word[0] in texttoindex:  # 키가 사전에 존재하는지 확인. 있는거만 저장
        cofindex = texttoindex[word[0]]  
        print(word[0], ":", cofindex, ":", indextocoef[cofindex])
        sol += indextocoef[cofindex]  # 문장 번호에 해당하는 가중치

#긍정(1), 부정(0)
if sol >=0:
    print(text, "=", y, "\n======긍정글 입니다. ")
else:
    print(text, "=", y, "\n======부정글 입니다. ")




















