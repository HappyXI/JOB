from django.shortcuts import render

# Create your views here.
def index(request):
    print('index')
    return render(request, "member/index.html")

def main(request):
    print('main')
    return render(request, "member/main.html")  