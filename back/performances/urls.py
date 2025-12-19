from django.urls import path
from . import views

app_name = "performances"
urlpatterns = [
    path("", views.index, name="index"),
    path("filter-genre/", views.filter_genre, name="filter_genre"),
    path("recommended/", views.recommended, name="recommended"),
    path("boxoffice-genre/", views.boxoffice_genre, name="boxoffice_genre"),
    path("<str:mt20id>/", views.performance_detail, name="detail"),
]
