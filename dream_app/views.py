
from django.shortcuts import render, redirect, HttpResponse 
from django.contrib import messages
import bcrypt
   
from .models import *

def reg_login(request): 
    return render(request, "loginreg.html")

def registration(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    confirm_pw = request.POST['confirm_pw']
    errors = User.objects.user_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return render(request, "loginreg.html")
    else:
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()   
        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], 
                    password=pw_hash) 
        user.save()
        request.session['userid'] = user.id
        return redirect('/dreams')

def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]     
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect('/dreams')
        else:
            messages.error(request, "Passwords don't match")
            return render(request, "loginreg.html")
    else:
        messages.error(request, "Email does not exist")
        return render(request, "loginreg.html")

def logout(request): 
    del request.session['userid']
    return redirect('/')

def dreams(request): 
    all_dreams_available = Dream.objects.exclude(access_level="PRV")
    my_favorite_dreams = []
    name = ""
    if 'userid' in request.session:
        user = User.objects.get(id=request.session['userid'])
        name = user.first_name

        for d in user.favorite_dreams.all():
            my_favorite_dreams.append(d)
        for d in user.dreams.all():
            my_favorite_dreams.append(d)          
           
    context = {
        'givenname': name,
        'all_dreams_available': all_dreams_available,
        'my_favorite_dreams': my_favorite_dreams
    }
    return render(request, "dashboard.html", context)



def createadream(request):
    user = User.objects.get(id=request.session['userid'])    
    name = user.first_name
    context = {
        'userid': request.session['userid'],
        'givenname': name,
    }
    return render(request, "create_a_dream.html", context)

def creating(request): 
    # title = request.POST['title']
    # description = request.POST['description']
    # key_words = request.POST['key_words']
    # access_level = request.POST['access_level']
    # print(access_level)

    errors = Dream.objects.dream_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return render(request, "create_a_dream.html")
    else:
        dream = Dream.objects.create(title=request.POST['title'], description=request.POST['description'], key_words=request.POST['key_words'],
                access_level=request.POST['access_level'], author=User.objects.get(id=request.session['userid']))
        
        return redirect('/dreams')

def viewadream(request, dreamid):
    dream = Dream.objects.get(id = dreamid)
    user = User.objects.get(id=request.session['userid'])    
    name = user.first_name     
    context = {
        'userid': request.session['userid'],
        'givenname': name,
        'dream': dream
    }
    return render(request, "view_a_dream.html", context)

# def editatrip(request, tripid):
#     user = User.objects.get(id=request.session['userid'])    
#     name = user.first_name
#     trip = Trip.objects.get(id = tripid)
#     context = {
#         'userid': request.session['userid'],
#         'givenname': name,
#         'trip': trip
#     }
#     return render(request, "edit_a_trip.html", context)

# def editing(request, tripid): 
#     trip = Trip.objects.get(id=tripid)
#     trip.owner=User.objects.get(id=request.session['userid']) 
#     trip.destination=request.POST['destination']
#     trip.start_date=request.POST['start_date']  
#     trip.end_date = request.POST['end_date']
#     trip.plan = request.POST['plan']

#     errors = Trip.objects.trip_validator(request.POST)
#     if len(errors) > 0:
#         for key, value in errors.items():
#             messages.error(request, value)
#         return redirect(f"/trips/edit/{tripid}")
#     else: 
#         trip.save()
#         return redirect('/trips')

# def deleteatrip(request, tripid):
#     trip_to_delete = Trip.objects.get(id =tripid)
#     trip_to_delete.delete()
#     return redirect('/trips')


# def returnajob(request, jobid):
#     job_return = Job.objects.get(id = jobid)
#     job_return.jobber = None
#     job_return.save()
#     return redirect('/jobs')

# def addajob(request, jobid):
#     job_to_take =Job.objects.get(id = jobid)
#     logged_user = User.objects.get(id = request.session['userid'])
#     job_to_take.jobber = logged_user
#     job_to_take.save()
#     return redirect('/jobs')




    


