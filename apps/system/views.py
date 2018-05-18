# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from .models import User, Appt
from django.contrib import messages
import bcrypt
from datetime import datetime
from django.db.models import Q
import pytz


def index(request):
    return render(request, 'blackbeltacquired/index.html')

def login(request):
    user = User.objects.get(email=request.POST['email'])
    status = User.objects.startlogin(request.POST)
    if status['verified'] == False:
        for error in status['error']:
            messages.error(request, error)
            return render(request, 'blackbeltacquired/index.html', status)
    else:
        request.session['user_id'] = user.id
        messages.success(request, 'Login successful.')

    return redirect(dashboard)

def logout(request):
    request.session.flush()
    return render(request, 'blackbeltacquired/index.html')

def register(request):
    status = User.objects.validation(request.POST)
    if status['valid']:
        User.objects.usercreator(request.POST)
        messages.success(request, 'Registration is successful, go ahead and login now.')
        return redirect('blackbeltacquired/index.html')
    else:
        for error in status['error']:
            messages.error(request, error)
        return redirect('blackbeltacquired/index.html')

def dashboard(request):
    taskedtoday = datetime.today()
    context = {
        'todayappt': Appt.objects.filter(date=taskedtoday).order_by('time'),
        'futureappt': Appt.objects.filter(date__gte=taskedtoday).exclude(date=taskedtoday),
        'taskedtoday': Appt.objects.filter(date=taskedtoday),
        'users': User.objects.get(id=request.session['user_id']),
        'today': datetime.now(tz=pytz.timezone('America/Vancouver')),
    }
    return render(request, 'blackbeltacquired/dashboard.html', context)

def addAppt(request):
    if request.POST['date'] == '' or request.POST['time'] == '' or request.POST['task'] == '':
        request.session['emptyfield_error'] = 'You cannot leave any field empty, try again'
        request.session['dupedatetime_error'] = ''
        request.session['emptyfield_error'] = ''
        return redirect(dashboard)

    date_time = request.POST['date'] + ' ' +  request.POST['time']
    if date_time <= str(datetime.now()):
        request.session['futuretime_error'] = 'You cannot time travel an appointment back in time. Try again.'
        request.session['emptyfield_error'] = ''
        request.session['dupedatetime_error'] = ''
        return redirect(dashboard)

    date_time = request.POST['date'] + request.POST['time']

    if not 'datetimecheck' in request.session:
        request.session['datetimecheck'] = []
    for dt in request.session['datetimecheck']:
        if date_time == dt:
            request.session['dupedatetime_error'] = 'You cannot have the exact same date and time for multiple appointments, try again.'
            request.session['emptyfield_error'] = ''
            request.session['futuretime_error'] = ''
            print(request.session['datetimecheck'])
            return redirect(dashboard)

    request.session['emptyfield_error'] = ''
    request.session['futuretime_error'] = ''
    request.session['dupedatetime_error'] = ''
    request.session['datetimecheck'].append(date_time)
    add = Appt.objects.createAppt(request.POST, request.session['user_id'])
    print(request.session['datetimecheck'])
    return redirect(dashboard)

def editAppt(request, appt_id):
    appt = Appt.objects.get(id=appt_id)
    request.session['appt_id'] = appt_id

    date = appt.date
    time = appt.time
    time.strftime('%H %M %S')

    context = {
        'appt': appt,
        'time': str(time),
        'date': str(date),
    }
    return render(request, 'blackbeltacquired/display.html', context)

def processApptUpdate(request):

    if request.POST['date'] == '' or request.POST['time'] == '' or request.POST['task'] == '':
        request.session['emptyfield_error'] = 'When editing an appt...You cannot leave any field empty, try again'
        request.session['dupedatetime_error'] = ''
        request.session['emptyfield_error'] = ''
        return redirect(dashboard)

    date_time = request.POST['date'] + ' ' +  request.POST['time']
    if date_time <= str(datetime.now()):
        request.session['futuretime_error'] = 'When editing an appt...You cannot time travel an appointment back in time. Try again.'
        request.session['emptyfield_error'] = ''
        request.session['dupedatetime_error'] = ''
        return redirect(dashboard)

    date_time = request.POST['date'] + request.POST['time']

    if not 'datetimecheck' in request.session:
        request.session['datetimecheck'] = []
    for dt in request.session['datetimecheck']:
        if date_time == dt:
            request.session['dupedatetime_error'] = 'When editing an appt...You cannot have the exact same date and time for multiple appointments, try again.'
            request.session['emptyfield_error'] = ''
            request.session['futuretime_error'] = ''
            print(request.session['datetimecheck'])
            return redirect(dashboard)

    request.session['emptyfield_error'] = ''
    request.session['futuretime_error'] = ''
    request.session['dupedatetime_error'] = ''
    request.session['datetimecheck'].append(date_time)
    process = Appt.objects.updateAppt(request.POST)
    return redirect(dashboard)

def deleteAppt(request):
    add = Appt.objects.destroyAppt(request.POST)
    return redirect(dashboard)

def display(request, user_id):
    return render(request, 'blackbeltacquired/display.html')
