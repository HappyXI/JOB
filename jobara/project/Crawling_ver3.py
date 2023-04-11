# pip install selenium
# pip install beautufulsoup4
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
    options = Options()
    options.headless = True  # 브라우저 창을 숨기도록 설정
    
    driver = webdriver.Chrome('/chromedriver/chromedriver.exe', options=options)
    
    #url 리스트 객체 초기화
    names = []
    fields = []
    urls = []
    idxs = []
    grades = []
    
    # URL 저장 진행도 표시
    for i in tqdm(range(start_page, end_page+1)):
    # for i in range(start_page,end_page+1):
        pagenum = i
        
        #url 접근
        search_url = f'https://www.jobkorea.co.kr/starter/PassAssay?Page={pagenum}&Pass_An_Stat=1'
        driver.get(search_url)
        # web loading 대기
        time.sleep(1)
        # 드라이버 현재 URL 로드 해서 response 객체에 저장
        response = requests.get(driver.current_url)
        # 뷰티풀소프를 이용해서 html 파싱
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 웹 스크래핑한 결과에서 필요한 정보를 추출하여 각 리스트에 append
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
        for grade in soup.select('.grade'): #전문가 별점 추가
            grade_text = grade.text.strip()
            grades.append(grade_text.strip())
        # print(f'{pagenum}/{end_page}')
   
    # 판다스 데이터프레임으로 저장
    data = {'name': names, 'field': fields,'grade': grades ,'url': urls}
    idxs = pd.to_numeric(idxs)
    df = pd.DataFrame(data, index = idxs)
    
    driver.quit()
    filename = f'init_{start_page}to{end_page}'
    df.to_csv(f'data/{filename}.csv', index=True)
    print(filename + ' 저장완료')
    return filename



def read_context(file_name):
    in_df = pd.read_csv(f'data/{file_name}', index_col=0)
    # 리스트 선언
    name = []
    field = []
    board_num = []
    A = []
    board_grade=[]
    P = []
   


    for url in tqdm(in_df['url']):
        try:
            response = requests.get(url)
            response.raise_for_status()
        except (requests.exceptions.HTTPError, requests.exceptions.RequestException):
            print(f'{url}에서 오류 발생. 다음 URL로 넘어갑니다.')
            continue

        soup = BeautifulSoup(response.text, 'html.parser')

        # 메뉴 text 제외하고 받아오기
        que_div_txs = soup.find_all('span', 'tx')[12:]
        ans_div_txs = soup.find_all('div', 'tx')[:len(que_div_txs)]

        # dl_con이 None인 경우 처리 추가
        if ans_div_txs is None:
            print(f'{url}에서 ans_div_txs을 찾을 수 없습니다. 다음 URL로 넘어갑니다.')
            continue

        # 기업명, 산업분류, 게시판번호 추가
        company_name = in_df.loc[in_df['url'] == url, 'name'].iloc[0]
        industry_field = in_df.loc[in_df['url'] == url, 'field'].iloc[0]
        board_number = in_df.loc[in_df['url'] == url, 'url'].iloc[0].split('View/')[1]
        board_grade = in_df.loc[in_df['url'] == url, 'grade'].iloc[0]


        # 답변 추출
        total_points = 0
        for ans_div_tx in ans_div_txs:
            points = 0
            # Qn 번째 답변에서 b 태그가 goot 이면 +1 bad면 -1
            for b_tag in ans_div_tx.find_all('b'):
                if 'good' in b_tag['class']:
                    points += 1
                elif 'bad' in b_tag['class']:
                    points -= 1

            # 파싱된 답변 데이터에서 span 태그와 'p'태그를 제외
            for tag in ans_div_tx('span'):
                tag.decompose()
            for tag in ans_div_tx('p'):
                tag.decompose()

            # 텍스트 추출 (col 구분이 ,이므로 모두 제거)
            answer = ans_div_tx.get_text(strip=True).replace(",", "").replace('\n', '').replace('\r', '')
            A.append(answer)
            total_points += points
            
        # 한 행이 끝나면 total_points를 P에 추가
        P.append(total_points)

            #total_sum
            #count_sum = board_grade + P
           # total_sum.append(count_sum)


    # 반복문이 끝난 후에 한 번만 추가합니다.
    name.extend([company_name] * len(ans_div_txs))
    field.extend([industry_field] * len(ans_div_txs))
    board_num.extend([board_number] * len(ans_div_txs))
    board_grade.extend([board_grade] * len(ans_div_txs))
    


    # DataFrame으로 변환
    out_df = pd.DataFrame({"기업명": name, "산업분류": field, "게시판번호": board_num, "답변": A, "별점": board_grade, "점수": P})
    out_df.to_csv(f'data/context_{file_name}', index=False, encoding='utf-8')
'''
def read_context(file_name):
    df = pd.read_csv(f'data/{file_name}', index_col=0)
    df.info()
    df['count_sum'] = out_df['board_grade'] + out_df['P']
    median_value = df['count_sum'].median()
    print("count_sum 컬럼의 중간값:", median_value)

'''

#### 필요한 과정만 주석 풀고 실행하시면 됩니다.
### 처음에 해당 폴더 내 ./data/ 디렉토리를 만들어야함
#==============================
# #총 이력서의 건수를 입력하세요 (처음에만, 전문가분석 조건 추가됐어요)
end_page = page_calc(20)

# 시작 페이지와 끝 페이지 입력 (url 불러오기)
init_data_url(1,end_page)

## url을 불러온 파일 이름을 실행시키면 됩니다!
read_context('init_1to1.csv')

