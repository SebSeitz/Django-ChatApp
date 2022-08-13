from email import message
from django.http import HttpResponseRedirect
from .models import Chat, Message
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login/')
def index(request):
   if request.method == 'POST':
      print("received data " + request.POST['textmessage'])
      myChat = Chat.objects.get(id=1)
      Message.objects.create(text=request.POST['textmessage'], chat=myChat, author=request.user, receiver=request.user)
   chatMessages = Message.objects.filter(chat__id=1) # Indenting is important here!
   return render(request, 'chat/index.html', {'messages': chatMessages})

def login_view(request):
   redirect = request.GET.get('next')
   if request.method == 'POST':
      user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
      if user:
         login(request, user)
         return HttpResponseRedirect(request.POST.get('redirect')) # get a get variable (=in url) to redirect
      else:
         return render(request, 'auth/login.html', {'wrongPassword':True, 'redirect': redirect} )
   return render(request, 'auth/login.html', {'redirect': redirect})

def register_user(request):
   if request.method == 'POST':
       password1=request.POST['password1']
       password2=request.POST['password2']
       username=request.POST['username']
       email=request.POST['email']

       if password1==password2:
            if User.objects.filter(username=username).exists():
               print('Username already taken')
               return render(request, 'auth/register.html', {'userTaken': True})
            elif User.objects.filter(email=email).exists():
               print('Email already taken')
               # messages.info(request, 'Email already taken')
               return render(request, 'auth/register.html', {'emailTaken': True})
            else:
               user =User.objects.create_user(username=username, email=email, password=password1)
               user.save()
               return render(request, 'auth/login.html', {'success': True})

       else:
          print('password not matching')
       return render(request, 'auth/register.html', {'noMatch': True})

   else:
          return render(request, 'auth/register.html')
