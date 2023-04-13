# -*- coding: utf-8 -*-

from django.urls import path, include
from . import views

urlpatterns = [
    path("index/", views.index, name = "index"),
    path("main/", views.main, name = "main"),
    path("join/", views.join, name = "join"),
    path("delete/<str:id>/", views.delete, name = "delete"),
    path("info/<str:id>/", views.info, name = "info"),
    path("login/", views.login, name = "login"),
    path("password/", views.password, name = "password"),
    path("picture/", views.picture, name = "picture"),
    path("update/<str:id>/", views.update, name = "update"),
    path("logout/", views.logout, name = "logout"),
    path("info/", views.infono, name = "infono"),
    path("update/", views.updateno, name = "updateno"),
    path("delete/", views.deleteno, name = "deleteno"),
]