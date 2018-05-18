# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import bcrypt, re, random
from django.db import models

class UserManager(models.Manager):
    def validation(request, postData):
        status = { 'valid' : True, 'error': [] }
        if not re.match(r'^[a-zA-Z ]+$', postData['name']) or not re.search(r'[a-zA-Z]{3,50}',postData['name']):
            status['valid'] = False
            status['error'].append('Your name must be at least 3 characters and no longer than 50, sucka.')
        if not re.match(r'^[a-zA-Z0-9 ]+$', postData['username'] or not re.search(r'[a-zA-Z0-9]{3,50}', postData['username'])):
            status['valid'] = False
            status['error'].append('Your username must be at least 3 characters and no longer than 50, sucka.')
        if not re.match(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', postData['email']):
            status['valid'] = False
            status['error'].append('Your email address sucks. Try again.')
        if len(User.objects.filter(email=postData['email'])) > 0:
            status['valid'] = False
            status['error'].append('That email has been taken.')
        if len(postData['password']) < 8:
            status['valid'] = False
            status['error'].append('Password has to be at least 8 characters long.')
        if not postData['password'] == postData['confirmpassword']:
            status['valid'] = False
            status['error'].append('Your password doesnt match.')
        if not postData['birthday']:
            status['valid'] = False
            status['error'].append('Please enter your birthday.')
        return status
    def startlogin(self, postData):
        user = User.objects.filter(email=postData['email'])
        status = {
            'verified' : False,
            'error' : 'Your email or password doesnt match.',
        }
        if len(user) > 0 and bcrypt.checkpw(postData['password'].encode(),user[0].password.encode()):
            status['user'] = user[0]
            status['verified'] = True

        return status

    def usercreator(self, postData):
        self.create(name=postData['name'],username=postData['username'],email=postData['email'],password=bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()), birthday=postData['birthday'])

class User(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    birthday = models.DateField(auto_now=False)
    objects = UserManager()
    def __repr__(self):
        return "<User object: {} {} {} {}>".format(self.name, self.username, self.email, self.password)

class ApptManager(models.Manager):
    def createAppt(self, postData, user_id):
        me = User.objects.get(id=user_id)
        self.create(task=postData['task'],time=postData['time'],date=postData['date'],madefor=me)
    def destroyAppt(self, postData):
        Appt.objects.get(id=postData['appt_id']).delete()
    def updateAppt(self, postData):
        appt = Appt.objects.get(id=postData['appt_id'])
        appt.task = postData['task']
        appt.time = postData['time']
        appt.date = postData['date']
        appt.status = postData['status']
        appt.save()

class Appt(models.Model):
    task = models.CharField(max_length=50)
    time = models.TimeField(auto_now_add=False)
    date = models.DateField(auto_now_add=False)
    status = models.CharField(max_length=50, default='pending')
    madefor = models.ForeignKey(User, related_name='appointments')
    objects = ApptManager()
    def __repr__(self):
        return "<|||APPOINTMENT - task: {} time: {} date: {} status: {}|||>".format(self.task, self.time, self.date, self.status)
