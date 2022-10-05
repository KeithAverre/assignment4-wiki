from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create_page", views.create_page, name="create_page"),
    path("<str:TITLE>", views.entry_page, name="TITLE"),
]
