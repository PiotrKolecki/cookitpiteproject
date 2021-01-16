from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from urllib.parse import parse_qs
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from . import models

import logging
import random 

def getRecommendedRecipes():
    recipesIds = models.Recipe.objects.values('id')
    randomIds = []
    recipesTargetNumber = 5

    if len(recipesIds) < 5:
        recipesTargetNumber = len(recipesIds)

    while len(randomIds) < recipesTargetNumber:
        randomId = random.choice(recipesIds)['id']

        if randomId not in randomIds:
            randomIds.append(randomId)

    recommendedRecipes = models.Recipe.objects.filter(pk__in=randomIds)
    
    return recommendedRecipes

def index(request):
    recommendedRecipes = getRecommendedRecipes()
    return render(request, 'home.html', {'recommendedRecipes': recommendedRecipes})

def loginRegisterUI(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/CookIT/account')
    else:
        decodedParams = parse_qs(request.body.decode('utf-8'))

        recommendedRecipes = getRecommendedRecipes()

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
                    return render(request, 'loginRegister.html', {'validationMsg': validationMsg, 'recommendedRecipes': recommendedRecipes})
           
            elif (decodedParams.keys() >= {"newLogin", "newPassword", "repeatPassword"}):
                username = request.POST['newLogin']
                password = request.POST['newPassword']
                password_repeat = request.POST['repeatPassword']

                if(password != password_repeat):
                    return render(request, 'loginRegister.html', {'validationMsg': 'Podane hasła nie są zgodne', 'recommendedRecipes': recommendedRecipes})
                else:
                    user = User.objects.create_user(username=username, password=password)
                    user.save()
                    return render(request, 'loginRegister.html', {'successMsg': 'Konto zostało utworzone', 'recommendedRecipes': recommendedRecipes})

        elif request.method == "GET":
            return render(request, 'loginRegister.html', {'recommendedRecipes': recommendedRecipes})

def logoutUI(request):
    if request.user.is_authenticated:
        logout(request)
        recommendedRecipes = getRecommendedRecipes()
        return render(request, 'loginRegister.html', {'successMsg': 'Wylogowano pomyślnie', 'recommendedRecipes': recommendedRecipes})
    return HttpResponseRedirect('/CookIT/')

def account(request):
    current_user = request.user
    if current_user.is_authenticated:
        current_user = request.user
        recommendedRecipes = getRecommendedRecipes()
        return render(request, 'userIdentity.html', {
            'username': current_user.username,
            'last_login': current_user.last_login,
            'first_name': current_user.first_name,
            'last_name': current_user.last_name,
            'email': current_user.email,
            'date_joined': current_user.date_joined,
            'recommendedRecipes': recommendedRecipes,
        })
    else:
        return HttpResponseRedirect('/CookIT/login')

def accountEdit(request):
    current_user = request.user
    if current_user.is_authenticated:
        decodedParams = parse_qs(request.body.decode('utf-8'))
        recommendedRecipes = getRecommendedRecipes()
        if request.method == "POST":
            if (decodedParams.keys() >= {"first_name", "last_name", "email"}):
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                email = request.POST['email']
                current_user.first_name = first_name
                current_user.last_name = last_name
                current_user.email = email
                current_user.save()
                return render(request, 'userEdit.html', {'successMsg': 'Poprawnie zapisano dane', 'recommendedRecipes': recommendedRecipes})

            else:
                validationMsg = "Coś poszło nie tak. Spróbuj ponownie później."
                return render(request, 'userEdit.html', {'validationMsg': validationMsg, 'recommendedRecipes': recommendedRecipes })

        elif request.method == "GET":
            return render(request, 'userEdit.html', {'recommendedRecipes': recommendedRecipes})
    else:
        return HttpResponseRedirect('/CookIT/login')

def category(request, id):
    fetchedCategory = models.Category.objects.get(id=id)
    fetchedRecipies = models.Recipe.objects.all().filter(category_id=id)
    recommendedRecipes = getRecommendedRecipes()

    return render(request, 'category.html', {
        'category_name': fetchedCategory.name,
        'category_description': fetchedCategory.description,
        'fetchedRecipies': fetchedRecipies,
        'recommendedRecipes': recommendedRecipes,
    })

def recipe(request, id):
    fetchedRecipie = models.Recipe.objects.get(id=id)
    ingredients = fetchedRecipie.ingredients.split('|')
    recipe_steps = fetchedRecipie.recipe_steps.split('|')
    fetchedRecipie.ingredients = ingredients
    fetchedRecipie.recipe_steps = recipe_steps
    fetchedRecipie.name = fetchedRecipie.name.upper()

    fetchedComments = models.Comment.objects.all().filter(recipe_id=id)

    recommendedRecipes = getRecommendedRecipes()
    return render(request, 'recipe.html', {
        'fetchedRecipie': fetchedRecipie,
        'fetchedComments': fetchedComments,
        'recommendedRecipes': recommendedRecipes,
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
        recommendedRecipes = getRecommendedRecipes()
        return render(request, 'addRecipe.html', {'recommendedRecipes': recommendedRecipes})
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

    recommendedRecipes = getRecommendedRecipes()
    return render(request, 'addRecipe.html', {'successMsg': 'Przepis został zapisany', 'recommendedRecipes': recommendedRecipes})

def userRecipes(request):
    if request.user.is_authenticated:
        user_id = request.user
        fetchedRecipies = models.Recipe.objects.all().filter(user_id=user_id)
    
        recommendedRecipes = getRecommendedRecipes()

        return render(request, 'userRecipes.html', {'fetchedRecipies': fetchedRecipies, 'recommendedRecipes': recommendedRecipes})
    else:
        return HttpResponseRedirect('/CookIT/login')

def removeRecipe(request):
    recipeId = request.POST.get('recipeIdToRemove')

    models.Comment.objects.filter(recipe_id=recipeId).delete()
    models.Recipe.objects.get(id=recipeId).delete()

    user_id = request.user
    fetchedRecipies = models.Recipe.objects.all().filter(user_id=user_id)
    
    recommendedRecipes = getRecommendedRecipes()

    return render(request, 'userRecipes.html', { 'fetchedRecipies': fetchedRecipies, 'recommendedRecipes': recommendedRecipes })

def editRecipePage(request, id):
    if request.user.is_authenticated:
        fetchedRecipie = models.Recipe.objects.get(id=id)
    
        recommendedRecipes = getRecommendedRecipes()

        return render(request, 'editRecipe.html', { 'fetchedRecipie': fetchedRecipie, 'recommendedRecipes': recommendedRecipes })
    else:
        return HttpResponseRedirect('/CookIT/')

def editRecipePost(request):
    categoriesDict = {
        "Śniadanie": 1,
        "Obiad": 2,
        "Kolacja": 3,
        "Deser": 4,
        "Przekąska": 5,
        "Inne": 6,
    }

    recipeId = request.POST.get('recipeId')
    recipeName = request.POST.get('recipeName')
    description = request.POST.get('description')
    ingredients = request.POST.get('ingredients')
    steps = request.POST.get('steps')
    category = request.POST.get('category')
    fetchedCategory = models.Category.objects.get(id=categoriesDict[category])

    models.Recipe.objects.filter(id=recipeId).update(
        category_id=fetchedCategory,
        name=recipeName,
        description=description,
        ingredients=ingredients,
        recipe_steps=steps,
    )

    fetchedRecipie = models.Recipe.objects.get(id=recipeId)
    
    recommendedRecipes = getRecommendedRecipes()

    return render(request, 'editRecipe.html', { 'fetchedRecipie': fetchedRecipie, 'recommendedRecipes': recommendedRecipes })

def userCommets(request):
    if request.user.is_authenticated:
        user_id = request.user
        fetchedComments = models.Comment.objects.all().filter(user_id=user_id)
    
        recommendedRecipes = getRecommendedRecipes()

        return render(request, 'userComments.html', {'fetchedComments': fetchedComments, 'recommendedRecipes': recommendedRecipes})
    else:
        return HttpResponseRedirect('/CookIT/login')

def removeComment(request):
    commentIdToRemove = request.POST.get('commentIdToRemove')

    models.Comment.objects.filter(id=commentIdToRemove).delete()

    user_id = request.user
    fetchedComments = models.Comment.objects.all().filter(user_id=user_id)
    
    recommendedRecipes = getRecommendedRecipes()

    return render(request, 'userComments.html', {'fetchedComments': fetchedComments, 'recommendedRecipes': recommendedRecipes})

def editCommentPage(request, id):
    if request.user.is_authenticated:
        fetchedComment = models.Comment.objects.get(id=id)
    
        recommendedRecipes = getRecommendedRecipes()

        return render(request, 'editComment.html', { 'fetchedComment': fetchedComment, 'recommendedRecipes': recommendedRecipes })
    else:
        return HttpResponseRedirect('/CookIT/')

def editCommentPost(request):
    commentId = request.POST.get('commentId')
    comment = request.POST.get('comment')
    rating = request.POST.get('rating')

    models.Comment.objects.filter(id=commentId).update(text=comment, rating=rating)

    fetchedComment = models.Comment.objects.get(id=commentId)
    
    recommendedRecipes = getRecommendedRecipes()

    return render(request, 'editComment.html', { 'fetchedComment': fetchedComment, 'recommendedRecipes': recommendedRecipes })
