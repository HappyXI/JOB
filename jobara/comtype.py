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


# comtype.csv 파일 읽기
df = pd.read_csv('com_type.csv')
df.info()

#파일 컬럼명 바꾸기
df.rename(columns={'게시판번호': 'board_num' , '11': 'thirties', '12': 'hundred' ,'13': 'big' , 
                    '14': 'public' , '15': 'foreign' , '16': 'mid', 
                    '17': 'offering' , '18': 'kosdaq'}, inplace=True) 
df.info()


df.to_sql(name='database_comtype', con=engine, if_exists='append', index=False)
