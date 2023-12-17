from django.shortcuts import render, redirect
from signup.models import Users


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
                    # return render(request, "index.html", {"results" : results})

                else:
                    return render(request, "message.html", {"message": "wrongpassword"})

        else:
            return render(request, "message.html", {"message": "account-no-exist"})

        # return render(request, "login/index.html", {"results" : results})

    if request.session.get("logged-in"):
        return redirect("/main")

    return render(request, "login/index.html")


