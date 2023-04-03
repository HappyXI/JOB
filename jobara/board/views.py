from django.shortcuts import render
from .models import Board
from django.http import HttpResponseRedirect
from . import textpredict # 자소서 분석 프로그램이 있는 모듈을 import

# Create your views here.
def index(request):
    print('index')
    return render(request, "board/index.html")

def job(request):
     if request.method !="POST" : #GET 방식일때
         return render(request, "board/job.html")
     
     else: # POST 방식 요청
         content = request.POST["content"]
         print(content)
         analysis_result = textpredict.analyze_text(content) # 자소서 분석 함수 호출
         print(analysis_result)
         msg = '긍정적인 자소서입니다.' if analysis_result == 1 else '부정적인 자소서입니다.'
         return render(request, "board/job.html", {'msg': msg})    #상단에 표시
