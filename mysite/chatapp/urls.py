from django.contrib import admin
from django.urls import path,include
from .import views

urlpatterns = [
    path('', views.RoomListView.as_view(), name='index'),
    path('<slug:slug>/', views.RoomDetailView.as_view(), name='chatroom'),
]