from django.urls import path, re_path
# from django.conf.urls import handler404

from . import views

# handler404 = views.handler_404

urlpatterns = [
    path('', views.index, name='index'),
    
    path('login/', views.loginRegisterUI, name='loginRegister'),
    path('logout/', views.logoutUI, name='logout'),

    path('account/', views.account, name='account'),
    path('account/identityEdit', views.accountEdit, name='accountEdit'),
    path('account/addRecipe', views.addRecipePage, name='addRecipePage'),
    path('account/userRecipes', views.userRecipes, name='userRecipes'),
    path('account/userRecipes/edit-<int:id>', views.editRecipePage, name='editRecipePage'),
    path('account/userComments', views.userCommets, name='userCommets'),
    path('account/userComments/edit-<int:id>', views.editCommentPage, name='editCommentPage'),

    path('c-<int:id>/', views.category, name='category'),
    path('r-<int:id>/', views.recipe, name='category'),

    path('addComment/', views.addComment, name='addComment'),
    path('addComment/sendData', views.addRecipePost, name='addRecipePost'),
    path('userRecipes/remove', views.removeRecipe, name='removeRecipe'),
    path('account/userRecipes/edit/sendData', views.editRecipePost, name='editRecipePost'),
    path('userComments/remove', views.removeComment, name='removeComment'),
    path('account/userComments/edit/sendData', views.editCommentPost, name='editCommentPost'),
]
