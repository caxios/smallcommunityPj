from django.shortcuts import render, redirect
from django.db.models import Q
from mainpage.models import Room, Topic
from mainpage.forms import RoomForm

# Create your views here.
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else '' # q is assigned value of string q when request intsance requests contain string q value..?
    rooms = Room.objects.filter(
        Q(topic__name__icontains= q) & 
        Q(name__icontains= q)
        
        ) # can filter what kinds of data i want to show 
    topics = Topic.objects.all()

    return render(request, 'home.html', {'rooms':rooms, 'topics':topics}) # can feed context data in form of dictionary

def room(request, pk):
    room = Room.objects.get(id=pk) # get(or collect..?) the Room instance that matches value of id to pk(all model instances get their own id automatically in created order)
    context = {'room':room}

    return render(request, 'room.html', context) # i can feed context(data) that can be used in certain html template(in this case context i created can be used in room.html file)

# these create, update, etc view functions can be replaced with class-based view which is offered by django
def createroom(request):
    form = RoomForm()

    if request.method == 'POST': # if request object's method is POST then,
        form = RoomForm(request.POST) # feed request.POST to ModelForm(in this case RoomForm)
        if form.is_valid(): # and if form is valid(valid in terms of satisfaction of required configuration of form, maybe)
            form.save() # save form which what user made(save just created instance of RoomForm instance, maybe)
            return redirect('main-home') # and redirect user to the url that has name main-home in string type
    context={'form':form}

    return render(request, 'room_form.html', context)

def updateroom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room) # this line of code let server knows what Room instance are we going to edit(update?), maybe
    context = {'form':form} # although in this view function it looks similar that context has same form data aboce createroom's form, they are different form, maybe

    if request.method == 'POST':
        form = RoomForm(request, instance=room)
        if form.is_valid:
            form.save()
            return redirect('main-home')

    return render(request, 'room_form.html', context)

def deleteroom(request, pk): # unlike create or update, delete function doesn't contain a form. because all tasks this function would do is just deleting data(record) from database table
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('main-home')
    return render(request, 'delete.html', {'obj':room})