# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 14:25:27 2023

@author: kch0325
"""

import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np
from konlpy.tag import Okt
from tqdm import tqdm
from collections import Counter
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
# 불용어정리
stopwords = ["있는", "그", "할", "이", "것", "하다", "그것", "이런", "하는", 
            "그런", "같은", "있다", "많은", "어떤", "이러한", "저", "때문에", 
            "에서", "그리고", "또는", "그러나", "그래서", "그렇게", "그렇지만", 
            "그때", "그들", "이것은", "그럼", "어떻게", "그러면", "이러한", 
            "그것이", "이것을", "그것은", "저는", "저의", "이러한", "저는", "저의",
            "그런데", "그러한", "그럴", "이렇게", "이상", "모든", "매우", "아주", 
            "정말", "너무", "그냥", "무엇인가", "무엇", "무슨", "어디", "누가", 
            "누구", "언제", "언젠가", "어느", "어떤", "이런", "저런", "하나", "둘",
            "셋", "넷", "다섯", "어쩌면", "어쨌든", '서','사항','나','하','년',
            "어떻게든", "어떤지", "어쩐지", "어쨌든", "어떤가요", "뭐", "어떡해", 
            "그게", "이게", "그거", "이거", "저거", "그저께", "어제", "오늘", 
            "내일", "모레", "이번", "그번", "저번", "내년", "작년", "그래서", 
            "그러니까", "그렇다면", "이러한", "같이", "함께", "열심히", "잘", 
            "매우", "진짜", "어쨌든", "그러면서", "물론", "뿐", "지와", "하셨나요",
            "최",'을','에','의','를','한','주','이','적','해','십','으로','하여',
            '시오','과','구체','대해','및','와','위해','하고','바랍니다','했던',
            '서술','은','후','된','등','가','수','중','하시오','하기','인','는',
            '가지','여','위','주세요','해주세요','이를','점','들','하게','최대',
            '이나','입','만의','때','니까','있다면','고','해주십시오','자','원',
            '로','지','대한','어떠한','에게','귀하','하십시오','이며','대하',
            '까지','성','큰','내','화','왜','하세요','하였는지','도','관','시',
            '하는지','예','상세','따라','간략히','있는지','끼친','했는지','단락',
            '항목','대','부분','못','삼','거나','되','남는','있어','이고','byte',
            '최대한','들어','으로서','기','에서의','하며','이었으며','함','인가요',
            '하고자','있습니까','임','줄','하신','더','하면서','히','기를','될',
            '하지','제','세','현','갖게','보다','있다고','시키기','게','과의','간',
            '내외','있을지','입니다','연','여러분','개','기와','있으면','또한','외',
            '계','형','하였던','되기','만','싶은지','하는데','키','워드','적용',
            '동','소','하십니까','되지','력','인해','했을','과는','한다면','정'
            '간략하게','Bytes','이었던','부항','께서','꼭','이하','합니다','전',
            '두','간의','자세하게','문항','된다고','교','바이트','있게','글자',
            '해보고','부문','여러','자세히','왔는지','택','시켜','않았을','귀하는',
            '온','My','안','야','되고','이라','라고','모두','먼저','단','경',
            '냈던','제외','출','약','회','받은','다','비해','적어주세요','군',
            '타','면','간단히','울','에도','불구','바를','사','합','있으며','A',
            '하였고','하시고','이라도','있도록','쓰시오','지어','아니라','하기에',
            '순','업','보십시오','까지의','bytes','당','이내','내의','지키기',
            '오','어','데','또','준','으로써','있었는지','해주시고','라는','으로서의',
            '있을','에는','아닌','되어야','했거나','씩','신','한다고','식','네',
            '이어야만', '나타낼','했습니까','양','싶으며','찾아서','강','하셨는지',
            '으로의','항','목별','상의','밖에','만큼','미만','What','바','됩니다',
            '간단하게','요약','이었거나','되었던','같습니다','구','어떠했는지','요',
            '뒤','영','직스','으로부터','you','스','하면','란','B','해야만','이라는',
            '어떠합니까','에서도','아니면','띄어쓰기','바라며','나를','후의','번',
            '하였을','되었을','지를','했으며','있겠는지를','주로','님','아는',
            '거쳤으며','있는지와','하시는지','적어주십시오','별로','ex','엔','주시길',
            'BYTE','이었나요','좋습니다','어떠하였는지','음','하셨던','했는지를',
            '좀','써','싶습니까','틀','라','이었고','했는지에','해주시','때문',
            '보세요','써주십시오','하는지와','있을지를','니','즈','라면','였으며',
            'ㅇ','있','a','하시어','하시오이내','싶으신','적으시오','트'
            ]

motiv_label = [ "한국환경공단에 입사하고자 하는 이유를 말해주세요.",
                "이 회사에 지원한 동기를 자세히 알려주세요.",
                "지원 동기가 무엇인가요?",
                "해당 분야에 지원한 이유를 말해주세요.",
                "이 회사에서 일하고 싶은 이유가 무엇인가요?",
                "입사하게 된 동기와 관련된 경험을 말씀해주세요.",
                "해당 직무에 대해 어떤 부분이 가장 매력적인가요?",
                "이 회사에 지원한 이유와 관련된 경험을 말씀해주세요.",
                "입사 후 어떤 분야에서 성장하고 싶으신가요?",
                "지원 동기와 관련된 본인의 경험을 약술해주세요.",
                "지원동기 및 입사후 포부"]

compet_label = ["업무 역량을 향상시키기 위해 노력했던 경험에 대해 이야기해주세요.",
                "이전 직장에서 본인이 맡은 프로젝트에 대해 설명해주세요.",
                "본인이 맡은 업무에서 발생한 문제 상황과 그에 대한 대처 과정에 대해 이야기해주세요.",
                "본인이 담당한 프로젝트에서 팀원과의 갈등 상황이 발생했다면, 어떻게 해결하였는지 이야기해주세요.",
                "업무 상황에서 느꼈던 가장 큰 어려움과 그것을 해결한 방법에 대해 이야기해주세요.",
                "자신이 맡은 프로젝트에서 어떤 성과를 이룩하였는지 이야기해주세요.",
                "본인의 역량 중에서 어떤 부분을 가장 강점으로 생각하고 있는지 이야기해주세요.",
                "자신이 성장할 필요가 있다고 생각하는 역량에 대해 이야기해주세요.",
                "이전에 맡았던 업무 중 가장 만족스러웠던 일이 무엇인지 이야기해주세요.",
                "본인이 담당한 업무에서 혁신적인 아이디어를 제안한 경험이 있다면, 그 아이디어에 대해 설명해주세요.",
                "업무역량"]

persnl_label = ["본인이 성격적으로 가진 강점과 약점은 무엇이며, 그 이유는 무엇인가요?",
                "어떤 가치관을 가지고 살아가고 있나요? 그리고 그 가치관은 어디서부터 기인했나요?",
                "고객이나 동료와 불만사항이나 문제가 발생했을 때, 본인이 그 상황을 어떻게 해결해 나갈 것인가요?",
                "성격적인 면에서 가장 자랑스러웠던 순간은 언제였나요? 그리고 그때 느꼈던 감정은 무엇인가요?",
                "본인이 다른 사람들과 다른 점, 독특한 점은 무엇이라고 생각하시나요?",
                "본인의 가치관이나 신념이 개인적으로 충돌하거나 힘들게 느껴지는 상황은 어떤 것이 있나요?",
                "당신이 무엇을 하고 싶은 이유는 무엇인가요? 그리고 그 이유가 어디서부터 기인했나요?",
                "성격적인 약점을 극복하기 위해 노력한 경험이 있다면, 그 경험에 대해 말해주세요.",
                "불확실한 상황에서의 대처능력이 필요한 일이 있을 때, 어떻게 대처하시나요?",
                "대인관계에서 어려운 상황이 생겼을 때, 본인은 어떻게 해결해 나가시나요?",
                "성격의 장단점 및 극복노력"]

groth_label = ["당신의 출신 지역은 어디이며, 그곳에서 어떤 경험을 했나요?",
                "가장 기억에 남는 어린 시절 경험은 무엇인가요?",
                "당신이 성장하며 겪은 가장 큰 어려움은 무엇이었나요?",
                "대학교에서 어떤 공부를 했으며, 그 공부를 선택한 이유는 무엇인가요?",
                "취업 준비를 하면서, 가장 어려웠던 경험은 무엇이었나요?",
                "당신의 성장에 가장 큰 영향을 끼친 사람은 누구이며, 어떤 영향을 끼쳤나요?",
                "어떤 일을 할 때, 가장 힘들어하는 부분은 무엇인가요?",
                "가장 좋아하는 취미나 관심사가 무엇인가요?",
                "새로운 분야나 일을 시작할 때, 스스로 동기부여를 하는 방법은 무엇인가요?",
                "당신이 가장 무서워하는 것은 무엇인가요? 그것을 극복하기 위해 노력한 경험이 있나요?",
                "성장과정및 경험"]


# 토큰화(tokenization)와 스테밍(stemming) 등의 과정을 거쳐서 단어 단위로 분리하고,
# 불용어(stopwords)를 제거하는 등의 작업을 수행합니다. 
# 이러한 전처리 과정을 거친 후에는 
# TF-IDF(term frequency-inverse document frequency)나
# 카운트 벡터화(count vectorization) 등의 
# 방법을 이용하여 각각의 질문에 대한 특징을 추출할 수 있습니다.

df = pd.read_csv(f'data/context_init_1to179.csv')

df.info()
df['질문'].head(20)

def text_cleaning(text):
    # 질문내 500자 1000자 등 텍스트 먼저 제거
    nnumber = re.compile('[0-9]+자')
    result = nnumber.sub("", text)
    nhangul = re.compile('[^ ㄱ-ㅣ 가-힣 a-zA-Z]+')
    result = nhangul.sub("",result)
    result = result.replace(" 이내","")
    return result

# 한글에선 스테밍(단어의 원형을 추출)이 잘 작동하지 않는다 함.

c_question = df['질문'].apply(text_cleaning).tolist()
okt = Okt()

# 토큰화 후 불용어 제거
Tokens = []
for question in tqdm(c_question):
    token = okt.morphs(question)
    token = [word for word in token if not word in stopwords]
    Tokens.append(token)

# 토큰 카운트
word_count = Counter([word for token in Tokens for word in token])

# for word, count in word_count.most_common():
#     if count < 10 or count >= 20:
#         continue
#     print("'"+word+"',""\n", count)

# 가장 많이 나오는 단어 50개 출력
word_count.most_common(50)


#토큰자료 시각화
plt.rc('font', family='Malgun Gothic')
most_common_words=word_count.most_common(20)

plt.figure(figsize=(12, 8))
plt.bar([word for word, count in most_common_words], [count for word, count in most_common_words])
plt.title('단어 빈도수')
plt.xlabel('단어')
plt.ylabel('빈도수')
plt.show()





















##분류 분석
####################
motiv_label
compet_label
persnl_label
groth_label

import pandas as pd

# 분류 리스트와 컬럼명
label_list = [motiv_label, compet_label, persnl_label, groth_label]
columns = ['category', 'Q']

# 각각의 리스트를 데이터프레임으로 변환하고 분류 컬럼 추가
dfs = []
for i, label in enumerate(label_list):
    df = pd.DataFrame(label, columns=[columns[1]])
    df[columns[0]] = i
    dfs.append(df)

# 데이터프레임 합치기
df_merged = pd.concat(dfs, ignore_index=True)

# 분류 값 변경
df_merged['category'] = df_merged['category'].replace({0: 'motiv', 1: 'compet', 2: 'persnl', 3: 'groth'})

df_merged




new_rows = pd.DataFrame({'Q': c_question, 'category': '미분류'})
df_merged = pd.concat([df_merged, new_rows])



# '미분류' 행 제거
train_data = df_merged[df_merged['category'] != '미분류']
train_data.info()
train_data['category'].value_counts()


# 텍스트 데이터를 수치화하기 위한 TfidfVectorizer 불러오기

# TfidfVectorizer 객체 생성
vectorizer = TfidfVectorizer(stop_words=stopwords,tokenizer=okt.morphs)

# 텍스트 데이터를 수치화
X_train = vectorizer.fit_transform(train_data['Q'])
y_train = train_data['category']



# 로지스틱 회귀 모델 생성
classifier = LogisticRegression(random_state=0)

# 모델 학습
classifier.fit(X_train, y_train)

# 확률 임계값 설정
threshold = 0.3

# '미분류' 행 선택
unclassified_data = df_merged[df_merged['category'] == '미분류']

# 텍스트 데이터 수치화
X_unclassified = vectorizer.transform(unclassified_data['Q'])

# 각 클래스에 대한 확률 예측
predicted_proba = classifier.predict_proba(X_unclassified)

# 최대 확률값과 해당 인덱스 찾기
max_proba = np.max(predicted_proba, axis=1)
predicted_class = classifier.classes_[np.argmax(predicted_proba, axis=1)]

# 최대 확률값이 임계값 미만이면 '미분류'로 설정
unclassified_data['분류_예측'] = np.where(max_proba < threshold, '미분류', predicted_class)

# 결과 확인
print(unclassified_data[['Q', '분류_예측']])


unclassified_data['분류_예측'].value_counts()


unclassified_data[unclassified_data['분류_예측'] == '미분류']['Q']















# 카테고라이징 된 csv 파일로 저장
# new_order = ['기업명', '산업분류','게시판번호', '질문','분류', '답변']
# df = df.reindex(columns=new_order)
# df.to_csv('data/categorizing.csv', index=False, encoding='utf-8')














# label_list = [motiv_label, compet_label, persnl_label, groth_label]

# for label in label_list:
#     for i in range(len(label)):
#         label[i] = text_cleaning(label[i])


# # 각 라벨에 대한 토큰 리스트 초기화
# motiv_label_tokens = []
# compet_label_tokens = []
# persnl_label_tokens = []
# groth_label_tokens = []

# #각 라벨 별 토크나이징
# for text in tqdm(motiv_label):
#     token = okt.morphs(text)
#     token = [word for word in token if not word in stopwords]
#     compet_label_tokens.append(token)

# for text in tqdm(compet_label):
#     token = okt.morphs(text)
#     token = [word for word in token if not word in stopwords]
#     motiv_label_tokens.append(token)

# for text in tqdm(persnl_label):
#     token = okt.morphs(text)
#     token = [word for word in token if not word in stopwords]
#     persnl_label_tokens.append(token)

# for text in tqdm(groth_label):
#     token = okt.morphs(text)
#     token = [word for word in token if not word in stopwords]
#     groth_label_tokens.append(token)

# motiv_label_tokens
# compet_label_tokens
# persnl_label_tokens
# groth_label_tokens


# # 토큰화된 label 데이터와 Y데이터 결합
# label_token_list = [motiv_label_tokens, compet_label_tokens, persnl_label_tokens, groth_label_tokens]
# columns = ['분류', '질문']
# # 각각의 리스트를 데이터프레임으로 변환하고 분류 컬럼 추가
# dfs = []
# for i, label in enumerate(label_token_list):
#     df = pd.DataFrame(label, columns=[columns[1]])
#     df[columns[0]] = i
#     dfs.append(df)

# # 데이터프레임 합치기
# df_merged = pd.concat(dfs, ignore_index=True)

# # 분류 값 변경
# df_merged['분류'] = df_merged['분류'].replace({0: 'motiv', 1: 'compet', 2: 'persnl', 3: 'groth'})


# df_merged


