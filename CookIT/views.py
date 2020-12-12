from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from urllib.parse import parse_qs

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
                # FIXME:
                # after check if user is in dataBase redirect to login page on error with error msg
                # return render(request, 'loginRegister.html', {'validationMsg': 'Login'})
                # or set cookie with expire date and redirect to account
                response = HttpResponseRedirect('/CookIT/account')
                response.set_cookie(key="userSession", value="sameValueAsInDB")
                return response
            elif (decodedParams.keys() >= {"newLogin", "newPassword", "repeatPassword"}):
                # FIXME:
                # after success user add set cookie and redirect to account 
                return render(request, 'loginRegister.html', {'validationMsg': 'Register'})

        elif request.method == "GET":
            return render(request, 'loginRegister.html')

def account(request):
    if request.COOKIES.get('userSession'): 
        test_param = "Account"
        return render(request, 'base.html', {'test_param': test_param})
    else:
        return HttpResponseRedirect('/CookIT/login')
