from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Users(models.Model):
    id = models.IntegerField(primary_key=True, blank=False, null=False, unique=True)
    username = models.CharField("Userame", max_length=30)
    email = models.EmailField("User Email", max_length=50)
    password = models.CharField("Password", max_length=30)
    photo = models.ImageField(upload_to='pfps/', null=True)

    def __str__(self):
        return self.username

class MessageInstances(models.Model):
    id = models.IntegerField(primary_key=True, blank=False, unique=True)
    type = models.CharField("Type", max_length=10, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    message = models.TextField(blank=True, max_length=1000, null=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

class Messages(models.Model):
    id = models.IntegerField(primary_key=True, blank=False, unique=True)
    incoming = models.ForeignKey(Users, related_name='incoming', blank=False, max_length=20, on_delete=models.CASCADE)
    outgoing = models.ForeignKey(Users, related_name='outgoing', blank=False, max_length=20, on_delete=models.CASCADE)
    message = models.ForeignKey(MessageInstances, related_name="directmessages", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.incoming}\t{self.outgoing}"

class Groups(models.Model):
    id = models.IntegerField(primary_key=True, blank=False, null=False, unique=True)
    name = models.CharField("Group name", max_length = 25)
    members = models.ManyToManyField(Users, related_name="members")
    admin = models.ManyToManyField(Users, related_name="admin")
    photo = models.ImageField(upload_to='pfps/', null=True)

    def __str__(self):
        return self.name


class GroupMessage(models.Model):
    id = models.IntegerField(primary_key=True, blank=False, null=False, unique=True)
    incoming = models.ForeignKey(Groups, related_name='gincoming', blank=False, max_length=20, on_delete=models.CASCADE)
    outgoing = models.ForeignKey(Users, related_name='goutgoing', blank=False, max_length=20, on_delete=models.CASCADE)
    message = models.ForeignKey(MessageInstances, related_name="groupmessages", on_delete=models.CASCADE)

