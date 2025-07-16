from django.urls import path 
from . import views



urlpatterns = [
    path('', views.log, name='log'),
    path('reg',views.reg),
    path('login/',views.login),
      path('home', views.home, name='home'),

    
    
]
    
