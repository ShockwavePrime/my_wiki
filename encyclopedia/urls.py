from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.view_entry, name="entry"),
    path("search/", views.search_view, name="search"),
    path("new/", views.new, name="new"),
    path("save/", views.save, name="save"),
    path("random/", views.random_entry, name="random_entry"),
    path("wiki/<str:title>/edit/", views.edit_entry, name="edit_entry"),
]
