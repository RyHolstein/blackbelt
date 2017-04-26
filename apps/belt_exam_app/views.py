from django.shortcuts import render, redirect
from .models import User, Destination
from django.contrib import messages
from django.db.models import Count
from django.core.urlresolvers import reverse
import datetime
# Create your views here.
def index(request):
    return render(request, 'belt_exam_app/index.html')
def travels(request):
    if 'id' not in request.session:
        return redirect('/not_logged')

    context = {
    'my_trips': Destination.objects.filter(user_id=request.session['id']),
    'user': User.objects.get(id=request.session['id']),
    'other_trips':  Destination.objects.exclude(user_id=request.session['id']),
    }
    return render(request, 'belt_exam_app/travels.html', context)

def destination(request, id):
    if 'id' not in request.session:
        return redirect('/not_logged')

    context = {
    'dest': Destination.objects.get(id=id),
    'users': User.objects.filter(joined=id)
    }

    return render(request, 'belt_exam_app/dest.html', context)

def add_travel(request):
    if 'id' not in request.session:
        return redirect('/not_logged')

    return render(request, 'belt_exam_app/add_travel.html')

def not_logged(request):
    return render(request, 'belt_exam_app/error.html')

def register_account(request):
    if request.method == 'POST':
        post_info = { #info requested from register form
            'name': request.POST['name'],
            'username': request.POST['username'],
            'password': request.POST['password'],
            'confirm_password': request.POST['confirm_password'],
        }
        result = User.objects.register(post_info)

        if result['errors'] == None:
            print result['user']
            request.session['id'] = result['user'].id
            messages.error(request, 'Login successful', extra_tags='signup')
            return redirect('/travels')
        else:
            for error in result['errors']:
                messages.error(request, error, extra_tags='signup') #print errors
            return redirect('/')

def login_account(request):
    if request.method == "POST":
        login_info = {  #info from login form
            'username': request.POST['username'],
            'password': request.POST['password'],
        }
    result = User.objects.login(login_info)

    if result['errors'] == None:
        request.session['id'] = result['user'].id #if fields match database
        messages.error(request, 'Login successful', extra_tags='login')
        return redirect('/travels')
    else:
        #if fields do not match database
        for error in result['errors']:
            messages.error(request, error, extra_tags='login')
        return redirect('/')

def logout(request):
    request.session.pop('id')
    messages.error(request, 'You have successfully been logged out', extra_tags='signup')
    return redirect('/')


def trip_add(request):
    trip_info = {
    'destination': request.POST['destination'],
    'descrip': request.POST['descrip'],
    'start_date': request.POST['start_date'],
    'end_date':request.POST['end_date'],
    'user_id': request.session['id'],
        }
    result = Destination.objects.add_travel(trip_info)
    if result['errors'] == None:
        print 'no errors'
        return redirect('/travels')
    else:
        for error in result['errors']:
            messages.error(request, error, extra_tags='add_trip')
    return redirect('travels/add')

def join_trip(request, id):
    add_data = {
    'trip_id': id,
    'user_id': request.session['id']
    }
    Destination.objects.add_user(add_data)
    return redirect('/travels')









#end end end
