from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = "dashboard"),
    path('chat/direct/<int:userid>', views.chat, name="chat"),
    path('chat/sendmessage', views.sendmessage, name = "message"),
    path('chat/sendimage', views.sendImage, name="send-image"),
    path('chat/fetch/<int:userid>', views.fetch, name = "fetch"),
    path('create/group', views.createGroup, name="create-group"),
    path('chat/group/<int:groupid>', views.groupChat, name="group-chat"),
    path('chat/fetch/group/<int:groupid>', views.fetchGroup, name = "fetchgroup"),
    path('chat/group/sendmessage', views.groupSendmessage, name="sendGroupMessage"),
    path('chat/group/sendimage', views.groupSendImage, name="sendGroupImage"),
    path('search/', views.search, name="search"),
    path('message/delete/', views.deleteMessage, name="deleteMessage"),
    path('api/', views.api, name="api"),
    path('logout', views.logout, name="logout")
]
