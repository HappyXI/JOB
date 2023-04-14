from django.shortcuts import render
from .models import Board
from .models import Mem_Resume
from django.utils import timezone
from django.http import HttpResponseRedirect
from . import textpredict # 자소서 분석 프로그램이 있는 모듈을 import
from intercept.intercepter import loginIdchk
from intercept.intercepter import loginChk
from django.core.paginator import Paginator


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

def company(request):
     if request.method !="POST" : #GET 방식일때
         return render(request, "board/company.html")
     
     else: # POST 방식 요청
         content = request.POST["content"]
         print(content)
         analysis_result = textpredict.analyze_text(content) # 자소서 분석 함수 호출
         print(analysis_result)
         msg = '긍정적인 자소서입니다.' if analysis_result == 1 else '부정적인 자소서입니다.'
         return render(request, "board/company.html", {'msg': msg})    #상단에 표
     
def samsung_textpredict(request):
     if request.method !="POST" : #GET 방식일때
         return render(request, "board/company.html")
     
     else: # POST 방식 요청
         content = request.POST["content"]
         print(content)
         analysis_result = samsung_textpredict.analyze_text(content) # 자소서 분석 함수 호출
         print(analysis_result)
         msg = '긍정적인 자소서입니다.' if analysis_result == 1 else '부정적인 자소서입니다.'
         return render(request, "board/company.html", {'msg': msg})    #상단에 표시
     
@loginIdchk
def resume(request, id):
    
    if request.method != "POST":
        try:
            resume = Mem_Resume.objects.get(id = id)
        except:
            resume = Mem_Resume(id = id, content = "")
        return render(request, "board/resume.html", {"resume":resume})
    
    else:
        resume = Mem_Resume(
            id = id,
            content = request.POST["content"],
            company = "",
            job = "")
        resume.save()
        
        context = {"msg" : "이력서 저장 완","url" : ""}
        print("resume 함수")
        print(context)
        return render(request, "alert.html", context)
    
def write(request):
    if request.method != "POST":
        try : 
            login = request.session["login"]
        except: # 로그아웃 상태 
            context = {"msg":"로그인하세요", "url":"/board/list/"}
            return render(request, "alert.html", context)
        
        return render(request, "board/write.html",{"login":login})
    else :          # POST 방식 요청
    #html에 {% csrf_token%}을 입력해야 함
        
        try:
            filename = request.FILES['file1'].name #업로드 파일의 이름
            #request.FILES['file1']: 업로드 파일 내용
            handle_upload(request.FILES["file1"])
        except : #업로드되는 파일이 없는 경우
            filename = ''
    
        b = Board(id = request.POST["id"],\
                  subject = request.POST["subject"],\
                  content = request.POST["content"],\
                  regdate = timezone.now(),\
                  readcnt = 0, file1 = filename)
        b.save()
        print("ok board") #db에 b 객체의 값이 저장. insert 실행
                          #num 기본키 값이 새값
        return HttpResponseRedirect('../list')

def list(request):
    
    #pageNum 파라미터를 정수형으로 변환
    #파라미터가 없으면 1이 기본값
    pagenum = int(request.GET.get("pageNum", 1))
    #모든 레코드 조회
    #order_by("-num") : num값의 내림차순 정렬
    #all_boards: 등록된 전체 게시물 목록
    all_boards = Board.objects.all().order_by("-num")
    #Paginator : all_boards 목록을 5개씩 묶어 분리 저장.
    paginator = Paginator(all_boards, 5)
    listcount = Board.objects.count()
    #paginator 객체에서 pageNum 번째 게시물 리턴
    #board_list : 페이지에서 출력할 게시물 목록 저장
    board_list = paginator.get_page(pagenum)
    #bottom page
    totalpage = (listcount//5) if listcount % 5 == 0 else (listcount//5) + 1
    start = ((board_list.number-1)//5)*5 + 1
    end = start + 4;
    if totalpage < end : end = totalpage
    page1 = board_list.paginator.page_range
    
    print("현재 페이지: ", board_list.number) #현제 페이지
    print("totalpage" , totalpage)
    
    return render(request, "board/list.html",\
                  {"board":board_list, "listcount":listcount, "page1": page1})
        
def info(request, num): #<int:num>
    board = Board.objects.get(num=num) #num(=column) = num 값에 해당하는 게시물 한 개 저장
    board.readcnt += 1
    board.save() #db에 조회건수 저장
    return render(request, "board/info.html", {"b":board})

def update(request, num):
    filename = ""
    if request.method != "POST":
        board = Board.objects.get(num=num)
        return render(request, "board/update.html", {"b":board})
    
    else : #POST 방식 요청
        filename = ''
        board = Board.objects.get(num=num)
        id1 = request.POST["id"]
        print(id1)
        if board.id != id1 : 
            context = {"msg":"작성자만 수정이 가능합니다", "url":"/board/update/" + str(num)}
            return render(request, 'board/alert.html', context)
    
    try : 
        filename = request.FILES["file1"].name
        handle_upload(request.FILES["file1"])
    except:
        filename = ""
    #file1이 업로드 되지 않으면 filename= request.POST["file2"]
    if filename == "":
        filename = request.POST["file2"]
    
    try:
        b = Board(num = num,\
                  id = request.POST["id"],\
                  subject = request.POST["subject"],\
                  content = request.POST["content"],\
                  file1 = filename
                  )
        b.save() #데이터가 있으면 update, 없으면 insert
        return HttpResponseRedirect('/board/info/' + str(num))
    except Exception as e:
        print(e)
        context = {"msg" : "게시물 수정 실패",\
                   "url" : "/board/update/"+str(num)}
        return render(request, "alert.html", context)

def delete(request, num):
    board = Board.objects.get(num = num)
    if request.session["login"] != board.id:
        context = {"msg" : "게시글 등록자만 삭제 가능합니다. 게시물 삭제 실패",\
                   "url" : "/board/list/"}
        return render(request, "alert.html", context)
    try:
        board.delete()
        return HttpResponseRedirect("/board/list")
    except:
        context = {"msg" : "게시물 삭제 실패",\
                   "url" : "/board/delete/"+str(num)}
        return render(request, "alert.html", context)
        
def handle_upload(f):
    #업로드 위치 : BASE_DIR/file/board/ 폴더 
    #f.name : 업로드 파일 이름
    with open("file/board/"+f.name, "wb") as dest:
        #f.chunks() : 업로드된 파일에서 버퍼만큼 읽기
        for ch in f.chunks():
            dest.write(ch) #출력파일에 저장
