from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.content, name="content"),
    path("newPage", views.newPage, name="newPage"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("random", views.randomPage, name="randomPage")
]
