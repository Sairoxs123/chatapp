from django.shortcuts import render
from .forms import SignupForm
from core.models import Users

# Create your views here.
def index(request):
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)

        if form.is_valid():
            error = False
            email = request.POST.get('email')
            name = request.POST.get('username')
            results = Users.objects.all()

            if len(name) > 10:
                error = "toolong"

            for i in results:
                if email == i.email:
                    error = "email"
                    break

                elif name == i.username:
                    error = "username"
                    break

                else:
                    error = False

            if error == False:
                form.save()
                return render(request, 'message.html', {'message' : 'signed'})

            if error == "email":
                return render(request, 'message.html', {'message' : 'email-exists'})

            if error == "username":
                return render(request, 'message.html', {'message' : 'username-exists'})

            if error == "toolong":
                return render(request, 'message.html', {'message' : 'toolong'})

    form = SignupForm
    results = Users.objects.all()
    return render(request, 'signup/index.html', {"form" : form, "results" : results})


def apiSignup(request):
    pass

