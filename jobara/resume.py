#pip install pymysql
#pip install sqlalchemy
import pandas as pd
import numpy as np
from sqlalchemy import create_engine  #db가져오기

# MySQL Connector using pymysql
import MySQLdb

from difflib import SequenceMatcher  #중복값 찾기 

# 데이터베이스 연결 정보 설정.   
db_user = 'kic'
db_password = '1111'
db_host = 'localhost'
db_port = '3306'
db_name = 'jobaradb'

# 데이터베이스 엔진 생성.
engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

# master에서 값 받아오기 
query = "select company_name, answer from database_database;"
resume_df = pd.read_sql_query(query, engine)
resume_df.info()



#1. resume 만들기 
'''  
key, ccode, jcode, answer
1, , ,  
2, , ,
3, , ,
'''

#1)ccode 생성
resume_df['company_ccode'] = resume_df['company_name']
resume_df.info()
#2) ccode 숫자값으로 변환하기 
query = "select * from database_company;"
company_df = pd.read_sql_query(query, engine)
company_df.info()

# company의 name이 resume의 company_ccode의 이름에 들어가 있는 행을 찾아 company의 ccode로 바꾸기
for idx, row in resume_df.iterrows():
    for _, company_row in company_df.iterrows():       
        if company_row['name'] in row['company_ccode']:
            resume_df.at[idx, 'ccode'] = company_row['ccode']
            break
        
resume_df['ccode'] = resume_df['ccode'].fillna(10) #나머지는 10
counts = resume_df['ccode'].value_counts()

print(counts)


#3) 직무코드 넣는 부분 ---> 지금은 없으니 우선 jcode 자리에 company_code를 넣겠습니다.
del resume_df['company_ccode']
resume_df['jcode'] = resume_df['ccode']

#4)key 생성
resume_df.insert(0, 'key', range(1, len(resume_df) + 1))

del resume_df['company_name']
resume_df.info()

#resume_df.to_csv('database_resume.csv', index=False)
#저장
resume_df.to_sql(name='database_resume', con=engine, if_exists='append', index=False)





