from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from urllib.parse import parse_qs
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from . import models

import logging

def index(request):
    return render(request, 'home.html')

def loginRegisterUI(request):
    if request.COOKIES.get('userSession'):
        return HttpResponseRedirect('/CookIT/account')
    else:
        decodedParams = parse_qs(request.body.decode('utf-8'))

        if request.method == "POST":
            if (decodedParams.keys() >= {"login", "password"}):
                username = request.POST['login']
                password = request.POST['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    response = HttpResponseRedirect('/CookIT/account')
                    response.set_cookie(key="userSession", value="sameValueAsInDB")
                    return response
                else:
                    validationMsg = "Użytkownik o podanych danych nie istnieje"
                    return render(request, 'loginRegister.html', {'validationMsg': validationMsg})
           
            elif (decodedParams.keys() >= {"newLogin", "newPassword", "repeatPassword"}):
                username = request.POST['newLogin']
                password = request.POST['newPassword']
                password_repeat = request.POST['repeatPassword']

                if(password != password_repeat):
                    return render(request, 'loginRegister.html', {'validationMsg': 'Podane hasła nie są zgodne'})
                else:
                    user = User.objects.create_user(username=username, password=password)
                    user.save()
                    return render(request, 'loginRegister.html', {'successMsg': 'Konto zostało utworzone'})

        elif request.method == "GET":
            return render(request, 'loginRegister.html')

def account(request):
    if request.COOKIES.get('userSession'): 
        current_user = request.user
        return render(request, 'userIdentity.html', {
            'username': current_user.username,
            'last_login': current_user.last_login,
            'first_name': current_user.first_name,
            'last_name': current_user.last_name,
            'email': current_user.email,
            'date_joined': current_user.date_joined
        })
    else:
        return HttpResponseRedirect('/CookIT/login')

def category(request, id):
    fetchedCategory = models.Category.objects.get(id=id)
    fetchedRecipies = models.Recipe.objects.all().filter(category_id=id)

    return render(request, 'category.html', {
        'category_name': fetchedCategory.name,
        'category_description': fetchedCategory.description,
        'fetchedRecipies': fetchedRecipies,
    })

def recipe(request, id):
    fetchedRecipie = models.Recipe.objects.get(id=id)
    ingredients = fetchedRecipie.ingredients.split('|')
    recipe_steps = fetchedRecipie.recipe_steps.split('|')
    fetchedRecipie.ingredients = ingredients
    fetchedRecipie.recipe_steps = recipe_steps

    fetchedComments = models.Comment.objects.all().filter(recipe_id=id)

    return render(request, 'recipe.html', {
        'fetchedRecipie': fetchedRecipie,
        'fetchedComments': fetchedComments,
    })

def addComment(request):
    comment = request.POST.get('comment')
    rating = request.POST.get('rating')
    recipeId = request.POST.get('recipeId')
    user_id = request.user

    newComment = models.Comment(text=comment, rating=rating, recipe_id=recipeId, user_id=user_id)
    newComment.save()

    return HttpResponseRedirect('/CookIT/r-' + recipeId)
