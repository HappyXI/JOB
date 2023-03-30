from django.shortcuts import render

# Create your views here.
def index(request):
    print('index')
    return render(request, "board/index.html")

def job(request):
    print('job')
    return render(request, "board/job.html")