from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
        path('api/get_place_id/', views.GetPlaceID.as_view(), name='get_place_id'),
        path('', views.index, name='index'),
]