#pip install konlpy
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import re
import numpy as np
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from konlpy.tag import Okt

df = pd.read_csv('data/context_init_1to179.csv', sep=',')

#한글, 공백, 숫자 영자부분만 전달
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



#점수 5,4=>긍정(1)
#점수 1,2,3 => 부정(0)  
df["y"]=df["점수"].apply(lambda x : 1 if float(x) > 3 else 0)
df.info()
df["y"].value_counts()


df['산업분류'] = df['산업분류'].apply(text_cleaning)
df['질문'] = df['질문'].apply(text_cleaning)
df['답변'] = df['답변'].apply(text_cleaning)
df['질문'] = df['질문'].str.replace('자 이내', '')
df['질문'] = df['질문'].str.replace('최소 자 최대 자 입력가능', '')
df['질문'] = df['질문'].str.replace('Bytes', '')
df['질문'] = df['질문'].str.replace('Byte', '')
df['질문'] = df['질문'].str.replace('bytes', '')
df['질문'] = df['질문'].str.replace('byte', '')
df['질문'] = df['질문'].str.replace(' 자 ', '')
df['질문'] = df['질문'].str.replace('글자수', '')
df['질문'] = df['질문'].str.replace(' 이내', '')

cleaned_df = df.copy()
cleaned_df.to_csv('data/cleaned_text.csv', index=False, encoding='utf-8')


# 텍스트 분류 함수 정의하기
def classify_question(text):
    # 형태소 분석기 객체 생성하기
    okt = Okt()
    
    # 텍스트에서 명사 추출하기
    nouns = okt.nouns(text)
    
    # 추출된 명사들이 어떤 분류 기준에 해당하는지 판단하기
    if any(word in text for word in motivation_words):
        return '지원동기'
    elif any(word in text for word in competency_words):
        return '직무역량'
    elif any(word in text for word in personality_words):
        return '성격의 장단점 및 가치관'
    elif any(word in text for word in aspiration_words):
        return '입사후 포부'
    elif any(word in text for word in gro_words):
        return '성정과정 및 배경'
    else:
        return '미분류'


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
# df_sample = df.sample(n=1000, random_state=999)
# df_sample['분류'] = df_sample['질문'].apply(classify_question)
# df_sample['분류'].value_counts()
# text_data = ' '.join(df_sample[df_sample['분류'] == '미분류']['질문'].astype(str))
# #############
df = pd.read_csv('data/cleaned_text.csv', sep=',')

df['분류'] = df['질문'].apply(classify_question)
# df['분류'].value_counts()

df_sample = df.sample(n=1000)
df_sample[df_sample['분류'] == '미분류']['질문'].head(30)


cates =['지원동기',
        '직무역량',
        '성격의 장단점 및 가치관',
        '성정과정 및 배경',
        '미분류',
        '입사후 포부']

    # 불용어 제거
stopwords = ['자', '대해', '시오', '및', '이내', '무엇', '그', '가장',
             '서술','위해', '작성', '중', '후', '것', '수', '등','점','대하',
             '포함','위','입','속']


# 한글 폰트 설정
plt.rc('font', family='Malgun Gothic')
# 단어카운팅 plot 그리기
for cate in cates :
    text_data = ' '.join(df[df['분류'] == f'{cate}']['질문'].astype(str))
    
    okt = Okt()
    
    # morphs = okt.morphs(text_data)
    nouns = okt.nouns(text_data)
    
    # 명사 단어 카운트
    counted_nouns = Counter(nouns)
    pos = okt.pos(text_data)
    # others = [word for word, tag in pos if tag != 'Noun']
    
    # # 명사를 제외한 다른 형태소 카운트
    # counted_others = Counter(others)
    
    for word in stopwords:
        del counted_nouns[word]
        # del counted_others[word]
    
    # 카운트 결과를 데이터프레임으로 변환
    df_count_nouns = pd.DataFrame.from_dict(counted_nouns, orient='index', columns=['count'])
    df_count_nouns.index.name = 'word'
    df_count_nouns = df_count_nouns.reset_index()
    
    # df_count_others = pd.DataFrame.from_dict(counted_others, orient='index', columns=['count'])
    # df_count_others.index.name = 'word'
    # df_count_others = df_count_others.reset_index()
    
    # 시각화
    plt.figure(figsize=(10, 6))
    sns.barplot(x='word', y='count', data=df_count_nouns.sort_values(by='count', ascending=False).iloc[:30])
    plt.xticks(rotation=45, ha='right')
    plt.title(f'{cate}')
    plt.show()
    
    # plt.figure(figsize=(10, 6))
    # sns.barplot(x='word', y='count', data=df_count_others.sort_values(by='count', ascending=False).iloc[:30])
    # plt.xticks(rotation=45, ha='right')
    # plt.show()




############### 미분류 => 분류로지스틱 회귀
#언더샘플링 => 자료가 많은 데이터를 적은수로 맞춤
#오버샘플링 => 자료가 적은 데이터를 많은 수에 맞춤


# '미분류' 행 제거
train_data = df[df['분류'] != '미분류'].sample(frac=0.8, random_state=1)
train_data.info()
train_data['분류'].value_counts()


# 텍스트 데이터를 수치화하기 위한 TfidfVectorizer 불러오기



# TfidfVectorizer 객체 생성
vectorizer = TfidfVectorizer(stop_words=stopwords)

# 텍스트 데이터를 수치화
X_train = vectorizer.fit_transform(train_data['질문'])
y_train = train_data['분류']



# 로지스틱 회귀 모델 생성
classifier = LogisticRegression(random_state=0)

# 모델 학습
classifier.fit(X_train, y_train)






# 확률 임계값 설정
threshold = 0.7

# '미분류' 행 선택
unclassified_data = df[df['분류'] == '미분류']

# 텍스트 데이터 수치화
X_unclassified = vectorizer.transform(unclassified_data['질문'])

# 각 클래스에 대한 확률 예측
predicted_proba = classifier.predict_proba(X_unclassified)

# 최대 확률값과 해당 인덱스 찾기
max_proba = np.max(predicted_proba, axis=1)
predicted_class = classifier.classes_[np.argmax(predicted_proba, axis=1)]

# 최대 확률값이 임계값 미만이면 '미분류'로 설정
unclassified_data['분류_예측'] = np.where(max_proba < threshold, '미분류', predicted_class)

# 결과 확인
# print(unclassified_data[['질문', '분류_예측']])


unclassified_data['분류_예측'].value_counts()


unclassified_data[unclassified_data['분류_예측'] == '미분류']['질문']

# 카테고라이징 된 csv 파일로 저장
new_order = ['기업명', '산업분류','게시판번호', '전문가총평', '질문','분류', '답변']
df = df.reindex(columns=new_order)
df.to_csv('data/categorizing.csv', index=False, encoding='utf-8')




# 단어 : 가중치 출력
vectorizer = TfidfVectorizer(stop_words=stopwords)
X_train = vectorizer.fit_transform(train_data['질문'])
y_train = train_data['분류']

classifier = LogisticRegression(random_state=0)
classifier.fit(X_train, y_train)

feature_names = vectorizer.get_feature_names()


# 각 클래스별로 단어별 가중치 출력
for i, category in enumerate(classifier.classes_):
    print(f'Category: {category}')
    coefs = classifier.coef_[i]
    word_coefs = sorted(zip(feature_names, coefs), key=lambda x: x[1], reverse=True)[:10]
    for word, coef in word_coefs:
        print(f'{word} : {coef:.3f}')
    print()

