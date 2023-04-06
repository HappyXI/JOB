from django.shortcuts import render
from .models import Member
from django.http import HttpResponseRedirect
import time
from datetime import datetime

# Create your views here.
def index(request):
    print('index')
    return render(request, "member/index.html")

def main(request):
    print('main')
    return render(request, "member/main.html")  

def join(request):
    if request.method != "POST":
        return render(request, "member/join.html")
    
    else:
        member = Member(id = request.POST["id"],\
                        name = request.POST["name"],\
                        pass1 = request.POST["pass"],\
                        gender = request.POST["gender"],\
                        tel = request.POST["tel"],\
                        email = request.POST["email"],\
                        picture= request.POST["picture"],\
                        address = request.POST["sample4_roadAddress"],\
                        address_detail= request.POST["sample4_detailAddress"],\
                        birthday = request.POST["birthday"])
        member.save() #insert 실행
        return HttpResponseRedirect("/member/login")

def delete(request):
    return render(request, "member/delete.html")

def info(request, id):
    member = Member.objects.get(id = id)
    birth = member.birthday.strftime("%Y-%m-%d")    
    
    return render(request, "member/info.html", {"mem":member})

def login(request):
    print("1: ", request.session.session_key)
    if request.method != "POST":
        return render(request, "member/login.html")
    else:
        id1 = request.POST["id"]
        pass1 = request.POST["pass"]
        try :
        #입력된 id값으로 Member 객체에서 조회
            member = Member.objects.get(id = id1)
            # member.pass1 : db에 등록된 비밀번호
            # pass1 : 입력된 비밀번호
            if member.pass1 == pass1:
                request.session["login"] = id1
                time.sleep(1)
                print("2: ", request.session.session_key)
                return HttpResponseRedirect("/member/main/")
            else:
                context = {"msg":"비밀번호가 틀립니다.","url":"/member/login/"}
                return render(request, "alert.html", context)
        except:
            context = {"msg":"아이디를 확인하세요","url":"/member/login/"}
            return render(request, "alert.html", context)            
        
        return HttpResponseRedirect("/member/main/")

def list(request):
    return render(request, "member/list.html")

def password(request):
    return render(request, "member/password.html")

def picture(request):
    if request.method != 'POST':
        return render(request, "member/pictureForm.html")
    else:
        #request.FILES["picture"] : 업로드된 파일 객체
        #fname : 파일 이름
        fname = request.FILES["picture"].name
        print(fname)
        handle_upload(request.FILES["picture"])
        return render(request, "member/picture.html", {"fname":fname})

def update(request,id):
    member = Member.objects.get(id = id)
    if request.method != "POST":    
        return render(request, "member/update.html", {"mem":member})
    else:
        # 비밀번호 검증
        # 비밀번호 오류 시 비밀번호 오류 메세지. update.html 페이지 출력
        # member.pass1 : db에 등록된 비밀번호
        # reauest.POST["pass"] : 입력된 비밀번호
        if request.POST["pass"] ==  member.pass1:
            member = Member(id = request.POST["id"],\
                            name = request.POST["name"],\
                            pass1 = request.POST["pass"],\
                            gender = request.POST["gender"],\
                            tel = request.POST["tel"],\
                            email = request.POST["email"],\
                            picture= request.POST["picture"],\
                            address = request.POST["sample4_roadAddress"],\
                            address_detail= request.POST["sample4_detailAddress"],\
                            birthday = request.POST["birthday"])
            member.save() #update 실행
            #member.delete() db에서 삭제
            return HttpResponseRedirect("/member/info/"+id+"/") #url
        else:
            context = {"msg":"비밀번호 오류입니다.",\
                       "url":"/member/update/"+id+"/"} #url
            return render(request, "alert.html",context)

def handle_upload(f):
    #업로드 위치 : BASE_DIR/file/member/ 폴더 
    #f.name : 업로드 파일 이름
    with open("file/member/"+f.name, "wb") as dest:
        #f.chunks() : 업로드된 파일에서 버퍼만큼 읽기
        for ch in f.chunks():
            dest.write(ch) #출력파일에 저장