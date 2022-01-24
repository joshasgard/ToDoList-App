from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo

def home(request):
    #Home page shown to user
    return render(request, 'todo/home.html')

def signupuser(request):
    #Sign up page and feature
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    else:
        # Create a new user
        if request.POST['password1'] ==request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'] )
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 
                            'error':'That username is already taken. Please choose a new username.'})
                #Tell user the username is already taken. 
        else:
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 
                            'error':'Passwords did not match'})
            #Tell user the passwords didn't match

def loginuser(request):
    # User login feature
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form': AuthenticationForm(), 'error':'Username and/or Password did not match'})
        else: 
            login(request, user)
            return redirect('currenttodos')

def logoutuser(request):
    #Log out feature
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def createtodo(request):
    #Form for users to create todo lists
    if request.method == 'GET':
        return render(request, 'todo/createtodos.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodos.html', {'form': TodoForm(), 'error':'Bad data passed in. Try again'})

def currenttodos(request):
    todos = Todo.objects.filter(user = request.user, datecompleted__isnull = True)
    return render(request, 'todo/currenttodos.html',{'todos':todos})

def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk)
    return render(request, 'todo/viewtodo.html',{'todo':todo})
