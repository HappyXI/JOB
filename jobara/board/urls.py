# -*- coding: utf-8 -*-

from django.urls import path, include
from . import views

urlpatterns = [
    path("index/", views.index, name = "index"),
    path("job/", views.job, name = "job"),
    path("company/", views.company, name = "company"),
    path("samsung_textpredict/", views.samsung_textpredict, name = "samsung_textpredict"),
]