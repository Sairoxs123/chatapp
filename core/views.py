from django.shortcuts import render, redirect
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

    return JsonResponse({"success": True})


def sendmessage(request):
    # This endpoint is now deprecated - using WebSockets instead
    # Kept for backward compatibility if needed
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

    data = {"success": True}

    return JsonResponse(data)


def search(request):
    query = request.GET.get("q")
    users = Users.objects.filter(username__contains=query)
    username = request.session.get("username")
    results = []

    for i in users:
        if i.username == username:
            continue
        else:
            results.append({
                'id': i.id,
                'username': i.username,
                'photo_url': i.photo.url if i.photo else ''
            })

    return JsonResponse({'users': results})


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
    message_list = []

    for i in messages:
        for j in results:
            if (
                str(i.incoming).strip() == str(username).strip()
                and str(i.outgoing).strip() == str(j.username).strip()
            ) or (
                str(i.incoming).strip() == str(j.username).strip()
                and str(i.outgoing).strip() == str(username).strip()
            ):
                message_data = {
                    'id': i.message.id,
                    'message': i.message.message,
                    'type': i.message.type,
                    'date': str(i.message.date),
                    'time': str(i.message.time),
                    'incoming': str(i.incoming),
                    'outgoing': str(i.outgoing),
                    'is_own': str(i.outgoing).strip() == str(username).strip()
                }
                
                if i.message.image:
                    message_data['image_url'] = i.message.image.url
                
                message_list.append(message_data)

    return JsonResponse({'messages': message_list})


def deleteMessage(request):
    mid = request.GET.get("id")
    MessageInstances.objects.get(id=mid).delete()

    return JsonResponse({"success": True})


def createGroup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        selected = request.POST.get("users")
        selected = selected.split(",")

        try:
            last = Groups.objects.last().id + 1

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
        return JsonResponse({"error": "Group does not exist"}, status=404)

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
            "group": group
        },
    )


def fetchGroup(request, groupid):
    group = Groups.objects.get(id=groupid)
    username = request.session.get("username")
    userinst = Users.objects.get(username=username)
    
    if userinst not in group.members.all():
        return JsonResponse({"error": "You are not added to this group."}, status=403)
    
    messages = GroupMessage.objects.filter(incoming=group)
    message_list = []

    for i in messages:
        message_data = {
            'id': i.message.id,
            'message': i.message.message,
            'type': i.message.type,
            'date': str(i.message.date),
            'time': str(i.message.time),
            'outgoing': str(i.outgoing.username),
            'photo_url': i.outgoing.photo.url if i.outgoing.photo else '',
            'is_own': str(i.outgoing.username) == username
        }
        
        if i.message.image:
            message_data['image_url'] = i.message.image.url
        
        message_list.append(message_data)

    return JsonResponse({'messages': message_list})

def groupSendmessage(request):
    # This endpoint is now deprecated - using WebSockets instead
    # Kept for backward compatibility if needed
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

    MessageInstances(id=pid, type=Type, message=message, date=date, time=time).save()

    p = MessageInstances.objects.get(id=pid)

    if image:
        p.image = image

    p.save()

    GroupMessage(incoming=group, outgoing=user, message=p).save()

    return JsonResponse({"success": True})


def api(request):
    return JsonResponse({"data":True})



def logout(request):
    request.session["logged-in"] = None
    request.session["id"] = None
    request.session["username"] = None
    request.session["email"] = None
    request.session["filename"] = None
    return redirect("/login")
