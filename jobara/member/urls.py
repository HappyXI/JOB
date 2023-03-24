# -*- coding: utf-8 -*-

from django.urls import path, include
from . import views

urlpatterns = [
    path("index/", views.index, name = "index"),
    path("main/", views.main, name = "main"),
]