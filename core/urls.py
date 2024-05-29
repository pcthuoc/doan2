from django.contrib import admin
from django.urls import path, include
from core import consumers
from datas import views as datas_views  
urlpatterns = [
    path('update/<str:api_key>/<str:pin>/', datas_views.update_value, name='update_value'),  #  http://.112.130:8000/update/TEY8OO5iafAV96gRKcZohbO6ED/V8/?value=10
    path('get/<str:api_key>/<str:pin>/', datas_views.get_value, name='get_value'),  
    path('admin/', admin.site.urls),          
  
    path("", include("apps.home.urls")) ,
 


                
]
