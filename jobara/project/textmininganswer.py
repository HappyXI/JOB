# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 15:09:46 2023

@author: gocu9778
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import re
import numpy as np
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from konlpy.tag import Okt

df = pd.read_csv('data/cleaned_textstar.csv', sep=',')


# 텍스트 분류 함수 정의하기
def classify_answer(text):
    # 형태소 분석기 객체 생성하기
    okt = Okt()
    
    # 텍스트에서 명사 추출하기
    nouns = okt.nouns(text)
    
    # 추출된 명사들이 어떤 분류 기준에 해당하는지 판단하기
    if any(word in text for word in motivation_words):
        return '지원동기답변'
    elif any(word in text for word in competency_words):
        return '직무역량답변'
    elif any(word in text for word in personality_words):
        return '성격의 장단점 및 가치관답변'
    elif any(word in text for word in aspiration_words):
        return '입사후 포부답변'
    elif any(word in text for word in gro_words):
        return '성정과정 및 배경답변'
    else:
        return '미분류답변'


# 분류 기준에 해당하는 단어들을 리스트로 정리하기
motivation_words = ['동기', '선택', '계기', '우리', '이유']
competency_words = ['역량','적합', '성취', '달성', '소통', 
                    '개발 경험', '협력', '서비스', '발휘', '구체적', '사용',
                    '직무관련', '보완', '지속', '직무기술', '프로젝트', '직무능력',
                    '공모전','전문기술','전문가','수행', '전문성', '이력', 'Skill',
                    'skill','스킬', ]
personality_words = ['성격', '가치관', '좋아', '대인관계', '열정',
                     '해결능력', '문제해결', '분석', '결정력', '장단점', '갈등',
                     '타인', '관계', '삶', '장점', '단점', '대립', '대처',
                     '입장', '부합','극복','충돌', '성품', '특성', '자기소개','자기소개서'
                     '좌우명', '생활신조', '사자성어', '교훈', '소개', '취미', '좌우명']
aspiration_words = ['포부', '목표', '계획', '비전', '비젼', '꿈', 'Vision', '다면'
                    , '기여', 'vision']
gro_words = ['성장배경', '성장','과정', '대학생활', '학창시절', '학교생활', '봉사']




#########데이터 샘플링
df = pd.read_csv('data/cleaned_textstar.csv', sep=',')

df['분류'] = df['답변'].apply(classify_answer)
# df['분류'].value_counts()
df_sample = df.sample(n=1000)
df_sample[df_sample['분류'] == '미분류']['답변'].head(30)


answers =['지원동기답변',
        '직무역량답변',
        '성격의 장단점 및 가치관답변',
        '성정과정 및 배경답변',        
        '입사후 포부답변',
        '미분류답변']

    # 불용어 제거
stopwords = ['수','것']


# 한글 폰트 설정
plt.rc('font', family='Malgun Gothic')
# 단어카운팅 plot 그리기
for answer in answers :
    text_data = ' '.join(df[df['분류'] == f'{answer}']['답변'].astype(str))
    
    okt = Okt()
    
    morphs = okt.morphs(text_data)
    # nouns = okt.nouns(text_data)
    
    # 명사 단어 카운트
   # counted_nouns = Counter(nouns)
    pos = okt.pos(text_data)
    others = [word for word, tag in pos if tag != 'Noun']    
    # # 명사를 제외한 다른 형태소 카운트
    counted_others = Counter(others)
    
    for word in stopwords:
        #del counted_nouns[word]
         del counted_others[word]
    
    # 카운트 결과를 데이터프레임으로 변환
    #df_count_nouns = pd.DataFrame.from_dict(counted_nouns, orient='index', columns=['count'])
    #df_count_nouns.index.name = 'word'
    #df_count_nouns = df_count_nouns.reset_index()
    
    df_count_others = pd.DataFrame.from_dict(counted_others, orient='index', columns=['count'])
    df_count_others.index.name = 'word'
    df_count_others = df_count_others.reset_index()
    
    # 시각화
    plt.figure(figsize=(10, 6))
    sns.barplot(x='word', y='count', data=df_count_others.sort_values(by='count', ascending=False).iloc[:30])
    plt.xticks(rotation=45, ha='right')
    plt.title(f'{answer}')
    plt.show()
    
    

    




