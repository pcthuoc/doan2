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
    path('addnguong/', views.addnguong , name = 'addnguong'),
    path('delete-hengio/<int:id>/', views.delete_hengio, name='delete_hengio'),
    path('delete-setnguong/<int:id>/', views.delete_setnguong, name='delete_setnguong'),
    path('edit-nguong/', views.edit_nguong, name='edit_nguong'),
    path('edit-gio/', views.edit_gio, name='edit_gio'),
    re_path(r'^.*\.*', views.pages, name='pages'),

]
