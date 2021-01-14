from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from urllib.parse import parse_qs
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from . import models

import logging

def index(request):
    return render(request, 'home.html')

def loginRegisterUI(request):
    if request.user.is_authenticated:
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

def logoutUI(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, 'loginRegister.html', {'successMsg': 'Wylogowano pomyślnie'})
    return HttpResponseRedirect('/CookIT/')

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

def accountEdit(request):
    current_user = request.user
    if current_user.is_authenticated:
        decodedParams = parse_qs(request.body.decode('utf-8'))
        if request.method == "POST":
            if (decodedParams.keys() >= {"first_name", "last_name", "email"}):
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                email = request.POST['email']
                current_user.first_name = first_name
                current_user.last_name = last_name
                current_user.email = email
                current_user.save()
                return render(request, 'userEdit.html', {'successMsg': 'Poprawnie zapisano dane'})

            else:
                validationMsg = "Coś poszło nie tak. Spróbuj ponownie później."
                return render(request, 'userEdit.html', {'validationMsg': validationMsg})

        elif request.method == "GET":
            return render(request, 'userEdit.html')
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
    fetchedRecipie.name = fetchedRecipie.name.upper()

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

def addRecipePage(request):
    if request.user.is_authenticated:
        return render(request, 'addRecipe.html')
    else:
        return HttpResponseRedirect('/CookIT/')
    
def addRecipePost(request):
    categoriesDict = {
        "Śniadanie": 1,
        "Obiad": 2,
        "Kolacja": 3,
        "Deser": 4,
        "Przekąska": 5,
        "Inne": 6,
    }

    recipeName = request.POST.get('recipeName')
    description = request.POST.get('description')
    ingredients = request.POST.get('ingredients')
    steps = request.POST.get('steps')
    category = request.POST.get('category')
    fetchedCategory = models.Category.objects.get(id=categoriesDict[category])
    user_id = request.user

    newRecipe = models.Recipe(
        user_id=user_id,
        category_id=fetchedCategory,
        name=recipeName,
        description=description,
        ingredients=ingredients,
        recipe_steps=steps,
    )
    newRecipe.save()

    return render(request, 'addRecipe.html', {'successMsg': 'Przepis został zapisany'})