from django.contrib import admin
from .models import *

# Register your models here.
#admin.site.register(Users)

@admin.register(Users)

class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')
    ordering = ('id',)
    search_fields = ('username', 'email')

@admin.register(MessageInstances)

class MessageInstancesAdmin(admin.ModelAdmin):
    list_display = ["id", "type", "message"]
    ordering = ["id"]


@admin.register(Messages)

class MessagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'incoming', 'outgoing')
    ordering = ('id', )
    search_fields = ('incoming', 'outgoing')

@admin.register(Groups)

class GroupsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    ordering = ['id']
    search_fields = ['name']

@admin.register(GroupMessage)

class GroupMessagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'incoming', 'outgoing')
    ordering = ('id', )
    search_fields = ('incoming', 'outgoing')

