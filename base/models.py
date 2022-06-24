from pyexpat import model
from statistics import mode
from tkinter import CASCADE
from tkinter.tix import Tree
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here.

class Topic(models.Model):
    name=models.CharField(max_length=200)

    def __str__(self):
     return self.name



class Room(models.Model):
    host= models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True) # 비어있어도 괜찬타.
    # message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True)
    # participants = 
    updated = models.DateTimeField(auto_now=True)  # auto now add : 한번 저장되면 변하지 않는 것이 add 붙이는것. auto now 는 항상 바뀐다. 
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name, self.topic

class Message(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    room = models.ForeignKey(Room, on_delete = models.SET_NULL, null=True)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)  # auto now add : 한번 저장되면 변하지 않는 것이 add 붙이는것. auto now 는 항상 바뀐다. 
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.updated, self.user, self.body