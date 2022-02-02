from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from mainpage.models import Room, Topic, Message
from mainpage.forms import RoomForm

# Create your views here.
def loginpage(request): # this can be replaced with django provided class-based view
    page = 'login'

    if request.user.is_authenticated:
        return redirect('main-home')
    
    if request.POST:
        username = request.POST.get('username') # get the value of what we named tag as username which is in this case a input tag. so get the value of input tag what user has entered 
        password = request.POST.get('password') # same as above

        try:
            user = User.objects.get(username=username) 
        except:
            messages.error(request, "User doesn't exist")
        
        user = authenticate(request, username=username, password=password) # give us user object when username and password are match which is inside of database

        if user is not None:
            login(request, user)
            return redirect('main-home')
        else:
            messages.error(request, "User name or password is not exist")

    context = {'page':page}
    return render(request, 'login_register.html', context)

def logoutuser(request):
    logout(request)
    return redirect('main-home')

def registeruser(request):
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('main-home')
        else:
            messages.error(request, "error occurred during registration")

    return render(request, 'login_register.html', {'form':form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else '' # q is assigned value of string q when request intsance requests contain string q value..?
    rooms = Room.objects.filter( # can filter what kinds of data i want to show 
        Q(topic__name__icontains= q) | 
        Q(name__icontains= q) |
        Q(description__icontains= q)
        
        )
    topics = Topic.objects.all()
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    return render(request, 'home.html', {'rooms':rooms, 'topics':topics, 'room_count':room_count, 'room_messages':room_messages}) # can feed context data in form of dictionary

def room(request, pk):
    room = Room.objects.get(id=pk) # get(or collect..?) the Room instance that matches value of id to pk(all model instances get their own id automatically in created order)
    message = room.message_set.all().order_by('-created') # get Message instances and order it by recently created time
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create( # create Message instance when a client requests 
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk = room.id)

    context = {'room':room, 'messages':message, 'participants':participants}
    
    return render(request, 'room.html', context) # i can feed context(data) that can be used in certain html template(in this case context i created can be used in room.html file)

def userprofile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    context = {"user":user, 'rooms':rooms}
    return render(request, 'profile.html', context)

# these create, update, etc view functions can be replaced with class-based view which is offered by django
@login_required(login_url='login')
def createroom(request):
    form = RoomForm()

    if request.method == 'POST': # if request object's method is POST then,
        form = RoomForm(request.POST) # feed request.POST to ModelForm(in this case RoomForm)
        if form.is_valid(): # and if form is valid(valid in terms of satisfaction of required configuration of form, maybe)
            form.save() # save form what user had made(save just created instance of RoomForm instance, maybe)
            return redirect('main-home') # and redirect user to the url that has name main-home in string type
    context={'form':form}

    return render(request, 'room_form.html', context)

@login_required(login_url='login') # this decorator let django to keep someone who do not logged in from doing something in certain view. in this case django require user to login if user want to update 
def updateroom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room) # this line of code let server knows what Room instance are we going to edit(update?), maybe
    context = {'form':form} # although in this view function it looks similar that context has same form data aboce createroom's form, they are different form, maybe

    if request.user != room.host: # check whether if a user who request this view function matches Room instance's user(which means the user who created Room instance)
        return HttpResponse('You are not allowed!')

    if request.method == 'POST':
        form = RoomForm(request, instance=room)
        if form.is_valid:
            form.save()
            return redirect('main-home')

    return render(request, 'room_form.html', context)

@login_required(login_url='login')
def deleteroom(request, pk): # unlike create or update, delete function doesn't contain a form. because all tasks this function would do is just deleting data(record) from database table
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed!')

    if request.method == 'POST':
        room.delete()
        return redirect('main-home')
    return render(request, 'delete.html', {'obj':room})

@login_required(login_url='login')
def deletemessage(request, pk): # unlike create or update, delete function doesn't contain a form. because all tasks this function would do is just deleting data(record) from database table
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed!')

    if request.method == 'POST':
        message.delete()
        return redirect('main-home')
    return render(request, 'delete.html', {'obj':message})