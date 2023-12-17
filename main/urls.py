from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = "dashboard"),
    path('chat/<int:userid>', views.chat, name="chat"),
    path('chat/sendmessage', views.sendmessage, name = "message"),
    path('chat/sendimage', views.sendImage, name="send-image"),
    path('chat/fetch/<int:userid>', views.fetch, name = "fetch"),
    path('search', views.search, name="fetch"),
    path('logout', views.logout, name="logout")
]
