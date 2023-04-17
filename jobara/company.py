# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 18:51:17 2023

@author: User
"""
#pip install pymysql
#pip install sqlalchemy==1.4.39
import pandas as pd
import numpy as np
from sqlalchemy import create_engine  #db가져오기

# MySQL Connector using pymysql
#pymysql.install_as_MySQLdb()
import MySQLdb

# 데이터베이스 연결 정보 설정.   
db_user = 'kic'
db_password = '1111'
db_host = 'localhost'
db_port = '3306'
db_name = 'jobaradb'

# 데이터베이스 엔진 생성.
engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
conn = engine.connect()


# master에서 값 받아오기 
query = "SELECT * FROM database_database"
df = pd.read_sql_query(query, engine)
df.info()

company = df["company_name"].unique()
print(company)


#1. 회사 디테일 컬럼 db 업로드
# ccode와 company_name 칼럼을 가지는 새로운 DataFrame 생성 
unique_companies = pd.DataFrame({'ccode': np.arange(1, len(company) + 1), 'company_name': company})
unique_companies.info()
#unique_companies.to_csv('database_companydetail.csv', index=False) 
unique_companies.to_sql(name='database_companydetail', con=engine, if_exists='append', index=False)



# 2. 회사컬럼 db 업로드
data = [
    {'ccode': 1, 'name': 'CJ'},
    {'ccode': 2, 'name': '씨제이'},
    {'ccode': 3, 'name': 'GS'},
    {'ccode': 4, 'name': '농협'},
    {'ccode': 5, 'name': 'NH'},
    {'ccode': 6, 'name': 'SK'},
    {'ccode': 7, 'name': '에스케이'},
    {'ccode': 8, 'name': '삼성'},
    {'ccode': 9, 'name': '한국전력'},
    {'ccode': 10, 'name': '기타'}
]
df = pd.DataFrame(data)
#df.to_csv('database_company.csv', index=False) 
df.to_sql(name='database_company', con=engine, if_exists='append', index=False)