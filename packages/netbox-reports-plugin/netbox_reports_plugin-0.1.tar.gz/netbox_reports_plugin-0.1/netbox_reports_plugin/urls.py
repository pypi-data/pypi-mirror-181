from django.urls import path

from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path('reports_device_list/', views.ReportsDeviceListView.as_view(), name='reports_device_list'),
    path('download_file/', views.download_file, name='download_file'),
]