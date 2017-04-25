from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from django.db.models import Count
from django.core.urlresolvers import reverse
import datetime
# Create your views here.
def index(request):
    return render(request, 'belt_exam_app/index.html')


def register_account(request):
    if request.method == 'POST':
        post_info = { #info requested from register form
            'f_name': request.POST['f_name'],
            'l_name': request.POST['l_name'],
            'email': request.POST['email'],
            'password': request.POST['password'],
            'confirm_password': request.POST['confirm_password'],
        }
        result = User.objects.register(post_info)

        if result['errors'] == None:
            print result['user']
            request.session['id'] = result['user'].id
            messages.error(request, 'Login successful', extra_tags='signup')
            return redirect('/')
        else:
            for error in result['errors']:
                messages.error(request, error, extra_tags='signup') #print errors
            return redirect('/')

def login_account(request):
    if request.method == "POST":
        login_info = {  #info from login form
            'email': request.POST['email'],
            'password': request.POST['password'],
        }
    result = User.objects.login(login_info)

    if result['errors'] == None:
        request.session['id'] = result['user'].id #if fields match database
        messages.error(request, 'Login successful', extra_tags='login')
        return redirect('/')
    else:
        #if fields do not match database
        for error in result['errors']:
            messages.error(request, error, extra_tags='login')
        return redirect('/')




















#end end end
