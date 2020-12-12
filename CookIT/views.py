from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from urllib.parse import parse_qs
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User

def index(request):
    test_param = "Hello"
    return render(request, 'base.html', {'test_param': test_param})

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
                    validationMsg = "credentials invalid"
                    return render(request, 'loginRegister.html', {'validationMsg': validationMsg})
           
            elif (decodedParams.keys() >= {"newLogin", "newPassword", "repeatPassword"}):
                username = request.POST['newLogin']
                password = request.POST['newPassword']
                password_repeat = request.POST['repeatPassword']

                if(password != password_repeat):
                    return render(request, 'loginRegister.html', {'validationMsg': 'Passwords don\'t match'})
                else:
                    user = User.objects.create_user(username=username, password=password)
                    user.save()
                    return render(request, 'loginRegister.html', {'validationMsg': 'Registered new user'})

        elif request.method == "GET":
            return render(request, 'loginRegister.html')

def account(request):
    if request.COOKIES.get('userSession'): 
        test_param = "Account"
        return render(request, 'base.html', {'test_param': test_param})
    else:
        return HttpResponseRedirect('/CookIT/login')
