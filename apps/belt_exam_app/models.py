from __future__ import unicode_literals
from django.db import models
from django.db.models import Count
import bcrypt, re, datetime
# EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def register(self, data):
        errors = []
        #form validations for firstname field
        if data['name'] == '':
            errors.append("Fields must not be Blank")
        elif len(data['name']) < 3:
            errors.append('The First Name field must be longer than 3 characters!')
        elif data['name'].isdigit():
            errors.append('The First Name can only be characters!')
        #form validations for email field


        if data['username'] == '':
            errors.append("Fields must not be Blank")
        elif len(data['username']) < 3:
            errors.append('The User field must be longer than 3 characters!')
        try:
            User.objects.get(username = data['username'])
            errors.append('Username is already being used')
        except:
            pass
        #form validations for password field
        if data['password'] < 8:
            errors.append('Password must be at least 8 characters long!')

        if not data['password'] == data['confirm_password']:
            errors.append('password fields have to match')
        print errors
        if len(errors) == 0:
            #add user to the database
            hashed = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            user = User.objects.create(name=data['name'], username=data['username'], password=hashed)
            return {'user': user, 'errors': None}
        else:
            return {'user': None, 'errors': errors}




    #Function for logging in
    def login(self, data):
        errors = []
        try:
            User.objects.get(username=data['username'])
            print 'same user'
            #email is already registered
        except:
            #email is NOT already registered
            print 'different user'
            errors.append('Username is incorrect')
            return {'user': None, 'errors':errors }

        if User.objects.get(username=data['username']).password.encode('utf-8') == bcrypt.hashpw(data['password'].encode('utf-8'), User.objects.get(username=data['username']).password.encode('utf-8')):
            user = User.objects.get(username=data['username'])
            print 'same pass'
            return {'user':user, 'errors': None}
        else:
            print 'different pass'
            errors.append('Pass is incorrect')
            return {'user': None, 'errors':errors }

class DestinationManager(models.Manager):
    def add_travel(self, data):
        errors = []
        if data['destination'] ==  '':
            errors.append('Destination cannot be blank')
        if data['descrip'] == '':
            errors.append('Description cannot be blank')
        if data['start_date'] == '':
            errors.append('Start cannot be blank')

        elif datetime.datetime.strptime(data['start_date'], '%Y-%m-%d') < datetime.datetime.now():
			errors.append("Your vacation must be in the future!!")


        if data['end_date'] == '':
            errors.append('End cannot be blank')
        if data["start_date"] > data['end_date']:
            errors.append('You cannot end before you start!!')

        if len(errors) == 0:
            user = User.objects.get(id=data['user_id'])
            print user.name
            destination = Destination.objects.create(destination=data['destination'], start_date=data['start_date'], end_date=data['end_date'], descrip=data['descrip'], created_by=user.name)
            destination.user_id.add(user)
            return {'errors': None}
        else:
            return {'errors': errors}

    def add_user(self, data):
        trip = Destination.objects.get(id = data['trip_id'])
        user = User.objects.get(id=data['user_id'])
        trip.user_id.add(user)
        return






# Create your models here.
class User(models.Model):
#Users
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Destination(models.Model):
    destination = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    descrip = models.TextField()
    created_by = models.CharField(max_length=100)
    user_id = models.ManyToManyField(User, related_name='joined')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = DestinationManager()
