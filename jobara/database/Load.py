# pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from asgiref.sync import sync_to_async
from database.models import Database
import pandas as pd
import io

# Google API credentials 파일 경로
creds_path = 'database/auth/auth.json'
token_path = 'database/auth/token.json'

# 사용자 인증 흐름 객체 생성
flow = InstalledAppFlow.from_client_secrets_file(
    creds_path,
    scopes=['https://www.googleapis.com/auth/drive']
)


# 사용자 인증 진행
creds = flow.run_local_server(port=8080)


# 인증 정보 저장
with open(token_path, 'w') as token_file:
    token_file.write(creds.to_json())

# 구글 API 권한 인증 및 빌드
service = build('drive', 'v3', credentials=creds)
# 파일 ID
file_id = '1paHKrII_xr09mDFSF_qKEd0_-sq7ng2f'

# 파일 속성 표시
file = service.files().get(fileId=file_id).execute()
print(file)


try:
    # 파일 정보 가져오기
    file = service.files().get(fileId=file_id).execute()

    # 파일 다운로드
    file_content = service.files().get_media(fileId=file_id).execute()

    # 바이너리 형식으로 다운로드한 파일 컨텐츠를 문자열로 변환
    content = file_content.decode('utf-8')

    # Pandas DataFrame으로 변환
    df = pd.read_csv(io.StringIO(content))
    print(df.head())

except HttpError as error:
    print(f'An error occurred: {error}')



@sync_to_async
def create_database_record(r):
    # board_num이 이미 존재한다면 해당 레코드를 무시하고 다음 레코드로 넘어갑니다.
    if Database.objects.filter(board_num=r[0]).exists():
        return
    # board_num이 존재하지 않는다면 새로운 레코드를 추가합니다.
    Database.objects.create(
        board_num=r[0],
        company_name=r[1],
        industry_classification=r[2],
        grade=r[3],
        score=r[4],
        answer=r[5]
    )

# 데이터프레임을 레코드로 변환
records = df.to_records(index=False)

# 레코드를 데이터베이스에 추가
for r in records:
    await create_database_record(r)