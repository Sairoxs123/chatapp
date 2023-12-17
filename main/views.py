from django.shortcuts import render, redirect, HttpResponse
from signup.models import Users, Messages
import json
from django.http import JsonResponse
from .forms import ImageForm


# Create your views here.
def index(request):
    if not request.session.get("logged-in") or not request.session.get("id"):
        return redirect("/login")

    else:
        users = Users.objects.all()
        return render(
            request,
            "index.html",
            {
                "id": request.session.get("id"),
                "username": request.session.get("username"),
                "email": request.session.get("email"),
                "url": request.session.get("filename"),
                "users": users,
            },
        )


"""
    if request.method == "POST":
        if results:
            incoming = Messages.objects.all().filter(incoming=request.session.get("username"), outgoing=userid)
            outgoing = Messages.objects.all()

        else:
            return render(request, "messages.html", {"message" : "account-no-exist"})
"""


def chat(request, userid):
    if not request.session.get("logged-in") or not request.session.get("id"):
        return redirect("/login")

    currentid = request.session.get("id")

    if userid == currentid:
        return render(request, "message.html", {"message" : "same"})

    users = Users.objects.all()
    results = Users.objects.all().filter(id=userid)
    username = request.session.get("username")
    messages = Messages.objects.all()
    main = []

    for i in messages:
        for j in results:
            if str(i.incoming).strip() == str(username).strip() and str(i.outgoing).strip() == str(j.username).strip():
                if str(i.type) == "image":
                    main.append(
                    f"""<div class="left" id="{i.id}">
                            <a href="/media/{str(i.image)}" target="_blank">
                                <img src=/media/{str(i.image)} id="text-img" style="width: 200px; height: 150px; border-radius: 22px;">
                            </a>
                        </div>"""
                    )

                    continue

                else:
                    main.append(
                    f"""<div class="left" id="{i.id}">
                            <span>{ i.message }</span>
                        </div>"""
                    )

                continue

            elif str(i.incoming).strip() == str(j.username).strip() and str(i.outgoing).strip() == str(username).strip():
                if str(i.type) == "image":
                    main.append(
                    f"""<div class="right" id="{i.id}">
                            <a href="/media/{str(i.image)}" target="_blank">
                                <img src=/media/{str(i.image)} id="text-img" style="width: 200px; height: 150px; border-radius: 22px;">
                            </a>
                        </div>"""
                    )

                    continue

                else:
                    main.append(
                    f"""<div class="right" id="{i.id}">
                            <span>{ i.message }</span>
                        </div>"""
                    )

                continue

    user = None

    for j in results:
        user = j.id

    return render(
        request,
        "chat.html",
        {
            "info": results,
            "id": request.session.get("id"),
            "username": request.session.get("username"),
            "email": request.session.get("email"),
            "url": request.session.get("filename"),
            "users": users,
            "senderid": user,
            "messages": main,
            "form":ImageForm
        }
    )

def sendImage(request):
    image = request.FILES.get("image")
    incoming = request.POST.get("incoming")
    outgoing = request.POST.get("outgoing")
    Type = request.POST.get("type")
    message = request.POST.get("message")

    userid = request.POST.get("userid")

    users = Users.objects.get(username=incoming)
    user = Users.objects.get(username=outgoing)

    if Messages.objects.all():
        pid = Messages.objects.all().last().id + 1
    else:
        pid = 0

    Messages(id=pid, incoming=users, outgoing=user, type=Type, message=message).save()

    p = Messages.objects.all().filter(id=pid)[0]

    if image:
        p.image = image

    p.save()

    return redirect(f"/main/chat/{userid}")

def sendmessage(request):
    #messageinput = request.POST.get("message")
    incoming = request.GET.get("incoming")
    outgoing = request.GET.get("outgoing")
    messageinput = request.GET.get("message")
    users = Users.objects.get(username=incoming)
    user = Users.objects.get(username=outgoing)

    Messages.objects.create(
        incoming=users, outgoing=user, type="text", message=messageinput
    )

    data = {
        "success"
    }

    return HttpResponse(data)

def search(request):
    query = request.GET.get("q")
    users = Users.objects.filter(username__contains=query)
    username = request.session.get("username")
    main = []

    for i in users:
        if i.username == username:
            continue
        else:
            main.append(f"""
                    <a href="/main/chat/{i.id}">
                        <div class="options">
                            <div class="option">
                                <div class="img">
                                    <img src="{ i.photo.url }" height="56" width="56" id="pfp">
                                </div>
                                <div class="user">
                                    <h3>{ i.username }</h3>
                                </div>
                            </div>
                        </div>
                    </a>
                        """)

    return HttpResponse(main)


def fetch(request, userid):
    results = Users.objects.all().filter(id=userid)
    username = request.session.get("username")
    messages = Messages.objects.all()
    main = []

    for i in messages:
        for j in results:
            if str(i.incoming).strip() == str(username).strip() and str(i.outgoing).strip() == str(j.username).strip():
                if str(i.type) == "image":
                    main.append(
                    f"""<div class="left" id="{i.id}">
                            <a href="/media/{str(i.image)}" target="_blank">
                                <img src=/media/{str(i.image)} id="text-img" style="width: 200px; height: 150px; border-radius: 22px;">
                            </a>
                        </div>"""
                    )

                    continue

                else:
                    main.append(
                    f"""<div class="left" id="{i.id}">
                            <span>{ i.message }</span>
                        </div>"""
                    )

                continue

            elif str(i.incoming).strip() == str(j.username).strip() and str(i.outgoing).strip() == str(username).strip():
                if str(i.type) == "image":
                    main.append(
                    f"""<div class="right" id="{i.id}">
                            <a href="/media/{str(i.image)}" target="_blank">
                                <img src=/media/{str(i.image)} id="text-img" style="width: 200px; height: 150px; border-radius: 22px;">
                            </a>
                        </div>"""
                    )

                    continue

                else:
                    main.append(
                    f"""<div class="right" id="{i.id}">
                            <span>{ i.message }</span>
                        </div>"""
                    )

                continue


    return HttpResponse(main)


def logout(request):
    request.session["logged-in"] = None
    request.session["id"] = None
    request.session["username"] = None
    request.session["email"] = None
    request.session["filename"] = None
    return redirect("/login")

