from django.urls import path, include
from . import views

urlpatterns = [
    path("index/", views.index, name = "index"),
    path("job/", views.job, name = "job"),
    path("company/", views.company, name = "company"),
    path("comtype/", views.comtype, name = "comtype"),
    path("resume/<str:id>/", views.resume, name = "resume"),
    path("update/<str:num>/", views.update, name = "update"),
    path("delete/<str:num>/", views.delete, name = "delete"),
    path("info/<str:num>/", views.info, name = "info"),
    path("list/", views.list, name = "list"),
    path("write/", views.write, name = "write"),
]
