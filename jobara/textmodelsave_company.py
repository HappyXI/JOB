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
import pickle
import os


import pandas as pd
from sqlalchemy import create_engine  #db가져오기

# MySQL Connector using pymysql
import MySQLdb

#from difflib import SequenceMatcher  #중복값 찾기 

# 데이터베이스 연결 정보 설정.   
db_user = 'kic'
db_password = '1111'
db_host = 'localhost'
db_port = '3306'
db_name = 'jobaradb'

# 데이터베이스 엔진 생성.
engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

companies = {
   'cj': [1, 2],
   'gs': 3,
   'nh': [4, 5],
   'sk': [6, 7],
   'ss': 8,
   'hj': 9
}
#한번에 돌려보자 
for company, ccode in companies.items():
    if isinstance(ccode, list):
        ccode_str = "(" + ",".join(str(c) for c in ccode) + ")"
    else:
        ccode_str = f"({ccode})"
    # master+resum에서 값 받아오기 
    query = f"SELECT r.answer, d.grade, d.score FROM database_resume r, database_database d \
        WHERE r.answer=d.answer AND r.ccode IN {ccode_str};"
    df = pd.read_sql_query(query, engine)
    df.info()


    #한글 형태소 분리 
    def get_pos(text): 
        okt= Okt()
        pos=okt.pos(text)
        pos =['{0}/{1}'.format(word,t) for word, t  in pos]
        return pos

    #1.글뭉치 변환하기: 단어들을 인덱스화
    #글뭉치: 분석을 위한 글모임
    index_vectorizer =CountVectorizer(tokenizer=lambda x : get_pos(x)) 
    df["answer"].tolist()
      
    #1. 형태소 분석에 의한 단어를 index화 했음 *** 
    X=index_vectorizer.fit_transform(df["answer"].tolist()) 
    X.shape  #(122, 6775)   cj
    
          
    #3-1) good_bad 칼럼 만들기.
    df["csum"] = df["grade"] + df["score"]
    df["good_bad"] = df["csum"]
          
    df.info()
    
    df["good_bad"].median()   # -2 
   
    m = df["good_bad"].median()
    s=df["csum"].tolist()
    
    df["good_bad"] = df["csum"].apply(lambda x: 1 if x > m else 0)
        
    df["good_bad"].value_counts()
    
    
    

    #2.가중치 확인 ***
     #X: 독립변수,  y: 종속변수 (1이상 긍정/0,음수 값 부정)
    tfidf_vectorizer = TfidfTransformer() 
    X = tfidf_vectorizer.fit_transform(X) #가중치만들기
    
    
    y=df["good_bad"]  #0: 부정, 1:긍정
    
        #훈련데이터,테스트 데이터로 분리
    x_train, x_test, y_train, y_test = train_test_split(X,y,test_size=0.3, random_state=3)
        
    #Logistic Regression 알고리즘을 이용하여 분류
    lr=LogisticRegression(random_state=0) #고정된 난수 생성
    lr.fit(x_train, y_train)
    
    y_pred=lr.predict(x_test)
    y_pred[:10]  #예측데이터


    # 평가하기 -- 값 확인해보기
    confmat = confusion_matrix(y_test, y_pred)
    print(confmat)
    
    
    # 정확도 출력
    accuracy = accuracy_score(y_test, y_pred)
    print(f"{company} - accuracy(정확도): {accuracy}")
    #cj - accuracy(정확도): 0.7567567567567568    ->  0.4864864864864865
    #gs - accuracy(정확도): 0.6785714285714286    ->  0.39285714285714285
    #nh - accuracy(정확도): 0.8571428571428571    ->  0.5714285714285714
    #sk - accuracy(정확도): 0.6944444444444444    ->  0.4634146341463415
    #ss - accuracy(정확도): 0.6833333333333333    ->  0.5333333333333333
    #hj - accuracy(정확도): 0.4117647058823529    ->  0.47058823529411764    
        
    
    model_dir = 'model'
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
         
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
    # 1) save dictionary : indextocoef
    with open(f'model/{company}_indextocoef.pkl', 'wb') as fp:
        pickle.dump(indextocoef, fp)
        print('dictionary saved successfully to file')
    
    # 2) save dictionary : texttoindex
    with open(f'model/{company}_texttoindex.pkl', 'wb') as fp:
        pickle.dump(texttoindex, fp)
        print('dictionary saved successfully to file')
    
    

