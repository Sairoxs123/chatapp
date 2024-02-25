from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.http import JsonResponse
import datetime
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request):
    if not request.session.get("logged-in") or not request.session.get("id"):
        return redirect("/login")


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
        return render(request, "message.html", {"message": "same"})

    users = Users.objects.all()
    results = Users.objects.all().filter(id=userid)

    user = None

    for j in results:
        user = j.id

    return render(
        request,
        "direct/chat.html",
        {
            "info": results,
            "id": request.session.get("id"),
            "username": request.session.get("username"),
            "email": request.session.get("email"),
            "url": request.session.get("filename"),
            "users": users,
            "senderid": user,
        },
    )


@csrf_exempt
def sendImage(request):
    image = request.FILES.get("image")
    incoming = request.POST.get("incoming")
    outgoing = request.POST.get("outgoing")
    Type = request.POST.get("type")
    message = request.POST.get("message")
    date = request.POST.get("date")
    time = request.POST.get("time")

    userid = request.POST.get("userid")

    print(incoming, outgoing)

    if Messages.objects.all():
        pid = MessageInstances.objects.last().id + 1
    else:
        pid = 1

    MessageInstances(id=pid, type=Type, message=message, date=date, time=time).save()

    p = MessageInstances.objects.get(id=pid)

    if image:
        p.image = image

    p.save()

    Messages(incoming=Users.objects.get(username=incoming), outgoing=Users.objects.get(username=outgoing), message=p).save()

    return redirect(f"/main/chat/{userid}")


def sendmessage(request):
    # messageinput = request.POST.get("message")
    incoming = request.GET.get("incoming")
    outgoing = request.GET.get("outgoing")
    messageinput = request.GET.get("message")
    users = Users.objects.get(username=incoming)
    user = Users.objects.get(username=outgoing)
    date = request.GET.get("date")
    time = request.GET.get("time")

    try:
        lid = MessageInstances.objects.last().id + 1

    except:
        lid = 1

    MessageInstances.objects.create(id=lid, type="text", message=messageinput, date=date, time=time)

    messageinst = MessageInstances.objects.get(id=lid)


    Messages.objects.create(
        incoming=users, outgoing=user, message=messageinst
    )

    data = {"success"}

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
            main.append(
                f"""
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
                        """
            )

    return HttpResponse(main)


def date_time(date, time):
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    date = date.split("-")
    date = datetime.date(int(date[0]), int(date[1]), int(date[2]))

    month = months[date.month - 1]

    day = days[date.weekday()]

    today = datetime.date.today()

    time = time.split(":")

    time.pop()

    if int(time[0]) > 12:
        time[0] = str(int(time[0]) - 12)
        time = ":".join(time)
        time += " p.m"

    else:
        time = ":".join(time)
        time += " a.m"

    if (today - date).days > 4:
        full_date = f"{month} {date.day}, {time}"

    elif today == date:
        full_date = f"Today, {time}"

    else:
        full_date = f"{day}, {time}"

    return full_date



def fetch(request, userid):
    results = Users.objects.all().filter(id=userid)
    username = request.session.get("username")
    messages = Messages.objects.all()
    main = []

    stored_date = None

    for i in messages:
        if stored_date != date_time(str(i.message.date), str(i.message.time)):
            main.append(f'''
                <main class="center">
                    <span>{date_time(str(i.message.date), str(i.message.time))}</span>
                </main>
                        ''')

            for j in results:
                if (
                    str(i.incoming).strip() == str(username).strip()
                    and str(i.outgoing).strip() == str(j.username).strip()
                    ):
                    if str(i.message.type) == "image":
                        main.append(
                            f"""<main class="left" id="{i.message.id}">
                                    <a href="/media/{str(i.message.image)}" target="_blank">
                                        <img src=/media/{str(i.message.image)} id="text-img" style="width: 200px; height: 150px; border-radius: 22px;">
                                    </a>
                                </main>"""
                        )

                        continue

                    else:
                        main.append(
                            f"""<main class="left" id="{i.id}">
                                <span id="message-{i.message.id}" contenteditable="true">{ i.message.message }</span>
                            </main>"""
                        )

                    continue

                elif (
                    str(i.incoming).strip() == str(j.username).strip()
                    and str(i.outgoing).strip() == str(username).strip()
                    ):
                    if str(i.message.type) == "image":
                        main.append(
                            f"""<main class="right" id="{i.message.id}">
                                <div class="menu-content">
                                    <button type="button" class="delete-btn" onclick="deleteMessage({i.message.id})">Delete</button>
                                </div>
                                <div class="menu">
                                    <button type="button" class="menu-btn" onclick="openMenu()">...</button>
                                </div>
                                <a href="/media/{str(i.message.image)}" target="_blank">
                                    <img src=/media/{str(i.message.image)} id="text-img" style="width: 200px; height: 150px; border-radius: 22px;">
                                </a>
                            </main>"""
                        )

                        continue

                    else:
                        main.append(
                            f"""<main class="right" id="{i.message.id}">
                                <div class="menu-content">
                                    <button type="button" class="delete-btn" onclick="deleteMessage({i.message.id})">Delete</button>
                                </div>
                                <div class="menu">
                                    <button type="button" class="menu-btn" onclick="openMenu()">...</button>
                                </div>
                                <span id="message-{i.message.id}" contenteditable="true">{ i.message.message }</span>
                            </main>"""
                        )

                    continue


        else:
            for j in results:
                if (
                    str(i.incoming).strip() == str(username).strip()
                    and str(i.outgoing).strip() == str(j.username).strip()
                    ):
                    if str(i.message.type) == "image":
                        main.append(
                            f"""<main class="left" id="{i.message.id}">
                                    <a href="/media/{str(i.message.image)}" target="_blank">
                                        <img src=/media/{str(i.message.image)} id="text-img" style="width: 200px; height: 150px; border-radius: 22px;">
                                    </a>
                                </main>"""
                        )

                        continue

                    else:
                        main.append(
                            f"""<main class="left" id="{i.id}">
                                <span id="message-{i.message.id}">{ i.message.message }</span>
                            </main>"""
                        )

                    continue

                elif (
                    str(i.incoming).strip() == str(j.username).strip()
                    and str(i.outgoing).strip() == str(username).strip()
                    ):
                    if str(i.message.type) == "image":
                        main.append(
                            f"""<main class="right" id="{i.message.id}">
                                <div class="menu-content">
                                    <button type="button" class="delete-btn" onclick="deleteMessage({i.message.id})">Delete</button>
                                </div>
                                <div class="menu">
                                    <button type="button" class="menu-btn" onclick="openMenu()">...</button>
                                </div>
                                <a href="/media/{str(i.message.image)}" target="_blank">
                                    <img src=/media/{str(i.message.image)} id="text-img" style="width: 200px; height: 150px; border-radius: 22px;">
                                </a>
                            </main>"""
                        )

                        continue

                    else:
                        main.append(
                            f"""<main class="right" id="{i.message.id}">
                                <div class="menu-content">
                                    <button type="button" class="delete-btn" onclick="deleteMessage({i.message.id})">Delete</button>
                                </div>
                                <div class="menu">
                                    <button type="button" class="menu-btn" onclick="openMenu()">...</button>
                                </div>
                                <span id="message-{i.message.id}">{ i.message.message }</span>
                            </main>"""
                        )

                    continue

    return HttpResponse(main)


def deleteMessage(request):
    mid = request.GET.get("id")
    MessageInstances.objects.get(id=mid).delete()

    return HttpResponse("done")


def createGroup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        selected = request.POST.get("users")
        selected = selected.split(",")

        try:
            last = Groups.objects.last() + 1

        except:
            last = 1

        group = Groups(id=last, name=name)

        group.save()

        for i in selected:
            inst = Users.objects.get(username=i)
            group.members.add(inst)
            group.save()

        admininst = Users.objects.get(username=selected[0])
        group.admin.add(admininst)
        group.save()

        return redirect(f"/main/chat/group/{last}")

    users = Users.objects.all()
    username = request.session.get("username")
    return render(
        request, "group/create-group.html", {"users": users, "username": username}
    )


def groupChat(request, groupid):
    if not request.session.get("logged-in") or not request.session.get("id"):
        return redirect("/login")

    users = Users.objects.all()
    results = Users.objects.all()

    try:
        group = Groups.objects.get(id=groupid)

    except:
        return HttpResponse("<center><h1>Group does not exist</h1></center>")

    return render(
        request,
        "group/chat.html",
        {
            "info": results,
            "id": request.session.get("id"),
            "username": request.session.get("username"),
            "email": request.session.get("email"),
            "url": request.session.get("filename"),
            "users": users,
            "groupid": groupid,
            "group":group
        },
    )


def fetchGroup(request, groupid):
    group = Groups.objects.get(id=groupid)
    username = request.session.get("username")
    userinst = Users.objects.get(username=username)
    if userinst not in group.members.all():
        return HttpResponse("You are not added to this group.")
    messages = GroupMessage.objects.all()
    main = []

    stored_date = None

    for i in messages:
        if stored_date != date_time(str(i.message.date), str(i.message.time)):
            main.append(f'''
                <main class="center">
                    <span>{date_time(str(i.message.date), str(i.message.time))}</span>
                </main>
                ''')
        if i.incoming == group:
            if str(i.outgoing) == username:
                if str(i.message.type) == "image":
                    main.append(
                        f"""<main class="right" id="{i.message.id}">
                            <div class="menu-content">
                                <button type="button" class="delete-btn" onclick="deleteMessage({i.message.id})">Delete</button>
                            </div>
                            <div class="menu">
                                <button type="button" class="menu-btn" onclick="openMenu()">...</button>
                            </div>
                            <a href="/media/{str(i.message.image)}" target="_blank">
                                <img src=/media/{str(i.message.image)} id="text-img" style="width: 200px; height: 150px; border-radius: 22px;">
                            </a>
                        </main>"""
                    )

                else:
                    main.append(
                        f"""<main class="right" id="{i.message.id}">
                                    <div class="menu-content">
                                        <button type="button" class="delete-btn" onclick="deleteMessage({i.message.id})">Delete</button>
                                    </div>
                                    <div class="menu">
                                        <button type="button" class="menu-btn" onclick="openMenu()">...</button>
                                    </div>
                                    <span id="message-{i.message.id}" contenteditable="true">{ i.message.message }</span>
                                </main>"""
                    )

            else:
                if str(i.message.type) == "image":
                    main.append(
                        f"""<main class="left" id="{i.id}">
                                <div class="image">
                                    <div class="name">
                                            {i.outgoing.username}
                                        </div>
                                    </div>
                                <div class="main">
                                    <img src="{i.outgoing.photo.url}" width="45" height="45" style="border-radius: 50%; margin-right: 0.5%;">
                                    <a href="/media/{str(i.message.image)}" target="_blank">
                                        <img src=/media/{str(i.message.image)} id="text-img" style="width: 200px; height: 150px; border-radius: 22px;">
                                    </a>
                                </div>
                            </main>"""
                    )

                else:
                    main.append(
                        f"""<main class="left" id="{i.id}">
                                <div class="image">
                                    <div class="name">
                                            {i.outgoing.username}
                                        </div>
                                    </div>
                                <div class="main">
                                    <img src="{i.outgoing.photo.url}" width="45" height="45" style="border-radius: 50%;">
                                    <span>{i.message.message}</span>
                                </div>
                            </main>"""
                    )

    return HttpResponse(main)

def groupSendmessage(request):
    incoming = request.GET.get("incoming")
    outgoing = request.GET.get("outgoing")
    messageinput = request.GET.get("message")

    group = Groups.objects.get(name=incoming)
    user = Users.objects.get(username=outgoing)
    date = request.GET.get("date")
    time = request.GET.get("time")

    try:
        lid = MessageInstances.objects.last().id + 1

    except:
        lid = 1

    print(lid)

    MessageInstances.objects.create(id=lid, type="text", message=messageinput, date=date, time=time)

    messageinst = MessageInstances.objects.get(id=lid)

    GroupMessage.objects.create(
        incoming = group, outgoing = user, message = messageinst
    )

    return JsonResponse({"success":True})


@csrf_exempt
def groupSendImage(request):
    image = request.FILES.get("image")
    incoming = request.POST.get("incoming")
    outgoing = request.POST.get("outgoing")
    message = request.POST.get("message")
    date = request.POST.get("date")
    time = request.POST.get("time")
    Type = "image"

    group = Groups.objects.get(name=incoming)
    user = Users.objects.get(username=outgoing)

    try:
        pid = MessageInstances.objects.last().id + 1

    except:
        pid = 1

    print(pid)

    MessageInstances(id=pid, type=Type, message=message, date=date, time=time).save()

    p = MessageInstances.objects.get(id=pid)

    if image:
        p.image = image

    p.save()

    GroupMessage(incoming=group, outgoing=user, message=p).save()

    return HttpResponse("success")


def api(request):
    return JsonResponse({"data":True})



def logout(request):
    request.session["logged-in"] = None
    request.session["id"] = None
    request.session["username"] = None
    request.session["email"] = None
    request.session["filename"] = None
    return redirect("/login")
