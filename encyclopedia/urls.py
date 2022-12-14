from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create_page/", views.create_page, name="create_page"),
    path("edit_page/<str:page>/", views.edit_page, name="edit_page"),
    path("entry_page/<str:TITLE>/", views.entry_page, name="entry_page"),
    path("entry_page/", views.entry, name="ent"),
    path("random_page/", views.random_page, name="random_page"),
]
