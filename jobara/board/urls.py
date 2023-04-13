# -*- coding: utf-8 -*-

from django.urls import path, include
from . import views

urlpatterns = [
    path("index/", views.index, name = "index"),
    path("job/", views.job, name = "job"),
    path("company/", views.company, name = "company"),
    path("samsung_textpredict/", views.samsung_textpredict, name = "samsung_textpredict"),
    path("resume/<str:id>/", views.resume, name = "resume"),
    path("update/<str:id>/", views.update, name = "update"),
    path("delete/", views.delete, name = "delete"),
    path("info/<str:id>/", views.info, name = "info"),
    path("list/", views.list, name = "list"),
    path("write/", views.write, name = "write"),
]