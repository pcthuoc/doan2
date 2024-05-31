# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    
    path('scene/', views.scene, name = 'scene'),
    path('addgio/', views.addgio , name = 'addgio'),
    path('chart/', views.chart , name = 'chart'),
    path('add_auto/', views.add_auto, name='add_auto'),


    path('delete-hengio/<int:id>/', views.delete_hengio, name='delete_hengio'),
    path('delete-auto/<int:id>/', views.delete_auto, name='delete_auto'),
    path('edit-gio/', views.edit_gio, name='edit_gio'),
    path('edit-auto/', views.edit_auto, name='edit_auto'),   
    path('edit-auto-value/', views.edit_auto_value, name='edit_auto_value'),


]
