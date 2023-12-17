from django.contrib import admin
from .models import *

# Register your models here.
#admin.site.register(Users)

@admin.register(Users)

class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')
    ordering = ('id',)
    search_fields = ('username', 'email')


@admin.register(Messages)

class MessagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'incoming', 'outgoing', 'message')
    ordering = ('id', )
    search_fields = ('incoming', 'outgoing')

