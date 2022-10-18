from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create_page/", views.create_page, name="create_page"),
    path("edit_page/<str:title>/", views.edit_page, name="edit_page"),
    path("entry_page/<str:title>/", views.entry_page, name="entry_page"),
    #path("entry_page/", views.entry, name="ent"),
    # Ah... I figured it out: The "ent" is the action of the search form. 
    # A easier-for-the-reader name would be "search" and views.search,
    path("search/", views.search, name="search"),
    path("random_page/", views.random_page, name="random_page"),
]
