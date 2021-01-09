from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginRegisterUI, name='loginRegister'),
    path('account/', views.account, name='account'),
    path('logout/', views.logoutUI, name='logout'),
]