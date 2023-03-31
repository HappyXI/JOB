#pip install selenium  
#pip install beautufulsoup4
import requests
import time
import pandas as pd
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm

def page_calc(tot_num):
    if tot_num % 20 == 0:
        max_page = tot_num // 20
    else:
        max_page = tot_num // 20 + 1
    return max_page

def init_data_url(start_page, end_page):
    #서칭된 url이 상대경로 이기때문에 앞부분 url을 따로 저장
    pre_url = 'https://www.jobkorea.co.kr'
    #드라이버 실행
    driver = webdriver.Chrome('/chromedriver/chromedriver.exe')
    options = Options()
    options.headless = True  # 브라우저 창을 숨기도록 설정
    
    driver = webdriver.Chrome('/chromedriver/chromedriver.exe', options=options)
    
    #url 리스트 객체 초기화
    grades=[]
    names = []
    fields = []
    urls = []
    idxs = []
    for i in range(start_page,end_page+1):
        pagenum = i
        #url 접근
        search_url = f'https://www.jobkorea.co.kr/starter/PassAssay?FavorCo_Stat=0&Pass_An_Stat=1&OrderBy=0&EduType=0&WorkType=0&isSaved=0&Page={pagenum}  '
        driver.get(search_url)
        # web loading 대기
        time.sleep(1)
        # 드라이버 현재 URL 로드 해서 response 객체에 저장
        response = requests.get(driver.current_url)
        # 뷰티풀소프를 이용해서 html 파싱
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 웹 스크래핑한 결과에서 필요한 정보를 추출하여 각 리스트에 append
        for grade in soup.select('.grade'): #전문가 별점 추가
            grade_text = grade.text.strip()
            grades.append(grade_text.strip())
                       
        for name in soup.select('.titTx'):
            names.append(name.text.strip())
        for field in soup.select('.field'):
            if field.text.strip() not in ['인턴', '신입']:
                fields.append(field.text.strip())
        for url in soup.find_all('p', {'class': 'tit'}):
            full_url = pre_url + url.find('a')['href']
            url_without_params = full_url.split('?')[0]
            urls.append(url_without_params)
            idx = full_url.split('View/')[1].split('?')[0]
            idxs.append(idx)
        print(f'{pagenum}/{end_page}')
       
        
    # 판다스 데이터프레임으로 저장
    data = {'name': names, 'field': fields, 'grade': grades, 'url': urls}
    idxs = pd.to_numeric(idxs)
    df = pd.DataFrame(data, index = idxs)
    
    driver.quit()
    filename = f'init_{start_page}to{end_page}'
    df.to_csv(f'data/{filename}.csv', index=True)
    print(filename + ' 저장완료')
    print(f'names: {len(names)}, fields: {len(fields)}, grades: {len(grades)}, urls: {len(urls)}, idxs: {len(idxs)}')

    return filename





def read_context(file_name):
    df = pd.read_csv(f'data/{file_name}',index_col=0)
    # texts 리스트선언
    cnt = 0
    texts = []
    # df데이터프레임 url컬럼만큼 반복. 
    for url in tqdm(df['url']):
        try:
            response = requests.get(url)
            response.raise_for_status()
        except (requests.exceptions.HTTPError, requests.exceptions.RequestException):
            print(f'{url}에서 오류 발생. 다음 URL로 넘어갑니다.')
            continue
        soup = BeautifulSoup(response.text, 'html.parser')
        dl_con = soup.find('dl', 'qnaLists')
        
        # dl_con이 None인 경우 처리 추가
        if dl_con is None:
            print(f'{url}에서 dl_con을 찾을 수 없습니다. 다음 URL로 넘어갑니다.')
            continue
    
        text = dl_con.text.split('질문Q')
        for i in range(1, len(text)):
            qna = text[i].split('보기\n\n\n답변')
            question = qna[0].replace('\n', '')
            answer = qna[1].replace('\n', '').replace('\r', '')
            answer = re.sub(r'글자수\s[\d,]+자[\d,]+Byte', '', answer)
            texts.append([df.loc[df['url'] == url, 'name'].iloc[0],
                          df.loc[df['url'] == url, 'field'].iloc[0],
                          df.loc[df['url'] == url, 'url'].iloc[0].split('View/')[1],
                          df.loc[df['url'] == url, 'grade'].iloc[0],
                          question,
                          answer])
        cnt += 1
        time.sleep(0.1)
    
    # DataFrame으로 변환
    qna_df = pd.DataFrame(texts, columns=['기업명', '산업분류','게시판번호' ,'점수', '질문', '답변'])
    
    # csv 파일로 저장
    qna_df.to_csv(f'data/context_{file_name}', index=False, encoding='utf-8')

    


#==============================
# #총 이력서의 건수를 입력하세요 (처음에만)
#end_page = page_calc(3570)
# 시작 페이지와 끝 페이지 입력 (url 불러오기)
#init_data_url(1,end_page)

## url을 불러온 파일 이름을 실행시키면 됨
read_context('init_1to179.csv')


