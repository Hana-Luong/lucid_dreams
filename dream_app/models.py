from __future__ import unicode_literals
from django.db import models
import re

from enum import Enum
class AccessLevel(Enum): 
    PUB = "Public"
    SUB = "Subscribers"
    PRV = "Private"

class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        if len(postData['first_name'])<2:
            errors['first_name'] = "First name should be at least 2 characters."
        if len(postData['last_name'])<2:
            errors['last_name'] = "Last name should be at least 2 characters."   
        if len(postData['password'])<8:
            errors["password"] = "Password should be at least 8 characters."
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):              
            errors["email"] = "Invalid email address!"       
        if (postData['password']) != (postData['confirm_pw']):
            errors["password"] =  "The two password fields must match."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password= models.CharField(max_length=255)
    confirm_pw= models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager() 
    # favorite_dreams = a list of dreams a given user likes
    # dreams

class DreamManager(models.Manager):
    def dream_validator(self, postData):
        errors = {}
        if len(postData['title']) < 1:
            errors["title"] = "Title is required!"
        if len(postData['description']) < 5:
            errors["description"] = "Description is at least 5 characters."      
        # How to handle the Key Words? and Access Level?   
        return errors

class Dream(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    key_words = models.CharField(max_length=15)
    author = models.ForeignKey(User, related_name="dreams", on_delete = models.CASCADE)
    user_who_like = models.ManyToManyField(User, related_name="favorite_dreams")
    # a list of users who like a given dream
    access_level = models.CharField(max_length=3, choices=[(tag, tag.value) for tag in AccessLevel])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = DreamManager() 

    def __str__(self):
        return "{} {} {}".format(self.id, self.title, self.access_level)



 







