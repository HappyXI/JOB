# -*- coding: utf-8 -*-

from django.shortcuts import render

def loginIdchk(func):
    def check(request, id):
        try : 
            login = request.session["login"]
        except:
            context = {"msg":"로그인하세요", "url":"/member/login/"}
            return render(request, "alert.html", context)
        else:
            if login != id  and login != 'admin':
                context = {"msg":"본인만 가능합니다.", "url":"/member/main/"}
                return render(request,"alert.html", context)
        return func(request,id)
    return check

    def check(request):
        context = {"msg":"로그인하세요", "url":"/member/login/"}
        return render(request, "alert.html", context)
        


def loginChk(func):
    def check(request, id):
        try : 
            login = request.session["login"]
        except: # 로그아웃 상태 
            context = {"msg":"로그인하세요", "url":"/member/login/"}
            return render(request, "alert.html", context)
        return func(request, id)
    return check

    def check(request):
        context = {"msg":"로그인하세요", "url":"/member/login/"}
        return render(request, "alert.html", context)

def adminChk(func):
    def check(request):
        try : 
            login = request.session["login"]
        except:
            context = {"msg":"로그인하세요", "url":"/member/login/"}
            return render(request, "alert.html", context)
        else:
            if login != "admin" and login != id:
                context = {"msg":"관리자만 가능합니다.", "url":"/member/main/"}
                return render(request, "alert.html", context)
        return func(request)
    return check

    def check(request):
        context = {"msg":"로그인하세요", "url":"/member/login/"}
        return render(request, "alert.html", context)