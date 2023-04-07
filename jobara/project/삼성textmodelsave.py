# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 09:27:04 2023

@author: User
"""
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score 
from konlpy.tag import Okt   
import pandas as pd
import pickle


#한글 형태소 분리 
def get_pos(text): 
    okt= Okt()
    pos=okt.pos(text)
    pos =['{0}/{1}'.format(word,t) for word, t  in pos]
    return pos

df=pd.read_csv("data/SK하이닉스(주).csv")
# 결측치 확인
print(df.isnull().sum())

# 결측치 제거
df = df.dropna()


#1.글뭉치 변환하기: 단어들을 인덱스화
#글뭉치: 분석을 위한 글모임
index_vectorizer =CountVectorizer(tokenizer=lambda x : get_pos(x)) 
df["답변"].tolist()

#형태소 분석에 의한 단어를 index화 했음
X=index_vectorizer.fit_transform(df["답변"].tolist())   
X.shape  #(13720, 56899)
for a in X[0]:
    print(a)
    print('============')
df["답변"].head()



#2.가중치 확인
#X: 독립변수,  y: 종속변수 (전문가 평점, 0~3:부정(0), 3~5:긍정(1))
tfidf_vectorizer = TfidfTransformer() 
X = tfidf_vectorizer.fit_transform(X) #가중치만들기
y=df["y"]  #0: 부정, 1:긍정
y
#훈련데이터,테스트 데이터로 분리
x_train, x_test, y_train, y_test = train_test_split(X,y,test_size=0.3, random_state=3)

#Logistic Regression 알고리즘을 이용하여 분류
lr=LogisticRegression(random_state=0) #고정된 난수 생성
lr.fit(x_train, y_train)

y_pred=lr.predict(x_test)
y_pred[:10]  #예측데이터
y_test.values[:10]  #실제데이터



#평가하기 -- 값 확인해보기 
confmat = confusion_matrix(y_test, y_pred)
confmat
#array([[3391,   46],   [[TN, FP],
#      [ 562,  117]],)   [FN, TP]]


#정확도 출력
print("accuracy(정확도) : " ,accuracy_score(y_test, y_pred))
#accuracy(정확도) :  0.8522837706511176



#model save
#1. 딕셔너리 생성
#1)text to index  텍스트를 가지고 인덱스를 찾는 것
texttoindex={}
for tt in list(index_vectorizer.vocabulary_): #dictionary key 만 list로 만들어진다
    word=tt.split("/")
    texttoindex[word[0]]=index_vectorizer.vocabulary_[tt]
texttoindex


#2)index to coef  가중치를 파악
indextocoef={}
for index, value in enumerate(lr.coef_[0]):
    indextocoef[index]=value


#save
#1)save dictionary : indextotext
with open('model/SKindextocoef.pkl','wb') as fp:
    pickle.dump(indextocoef, fp)
    print('dictionary saved successfully to file')

#2)save dictionary : texttoindex
with open('model/SKtexttoindex.pkl','wb') as fp:
    pickle.dump(texttoindex, fp)
    print('dictionary saved successfully to file')


#3)Logistic Regression save
filename = 'model/SKlregression.rl'
pickle.dump(lr, open(filename,'wb'))



#modle read
with open('model/SKindextocoef.pkl', 'rb') as fp:
    indextocoef = pickle.load(fp)
indextocoef

with open('model/SKtexttoindex.pkl', 'rb') as fp:
    texttoindex = pickle.load(fp)
texttoindex

lr = pickle.load(open('model/SKlregression.rl', 'rb'))
lr.coef_[0]



