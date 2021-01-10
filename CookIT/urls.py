from django.urls import path, re_path
# from django.conf.urls import handler404

from . import views

# handler404 = views.handler_404

urlpatterns = [
    path('', views.index, name='index'),
    
    path('login/', views.loginRegisterUI, name='loginRegister'),
    path('logout/', views.logoutUI, name='logout'),

    path('account/', views.account, name='account'),
    path('account/edit', views.accountEdit, name='accountEdit'),

    path('c-<int:id>/', views.category, name='category'),
    path('r-<int:id>/', views.recipe, name='category'),

    path('addComment/', views.addComment, name='addComment'),
]
