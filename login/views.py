from django.shortcuts import render, redirect
from core.models import Users
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


# Create your views here.
def index(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        results = Users.objects.all().filter(username=username)

        if results:
            for i in results:
                if password == i.password:
                    request.session["logged-in"] = True
                    request.session["id"] = i.id
                    request.session["username"] = i.username
                    request.session["email"] = i.email
                    request.session["filename"] = i.photo.url
                    return redirect("/main")

                else:
                    return render(request, "message.html", {"message": "wrongpassword"})

        else:
            return render(request, "message.html", {"message": "account-no-exist"})


    if request.session.get("logged-in"):
        return redirect("/main")

    return render(request, "login/index.html")


@csrf_exempt
def apiLogin(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    try:
        result = Users.objects.get(username=username)

    except:
        return JsonResponse({"result":False})

    if result.password == password:
        return JsonResponse({"result":True})

    return JsonResponse({"result":"Incorrect password"})
