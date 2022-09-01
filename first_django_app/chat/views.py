from email import message
from django.http import HttpResponseRedirect
from .models import Chat, Message
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers # means that an object is being transformed into the correct form

# Create your views here.
@login_required(login_url='/login/')
def index(request):
   if request.method == 'POST':
      print("received data " + request.POST['textmessage'])
      myChat = Chat.objects.get(id=1)
      new_message = Message.objects.create(text=request.POST['textmessage'], chat=myChat, author=request.user, receiver=request.user)
      serialized_obj = serializers.serialize('json', [new_message])
      return JsonResponse(serialized_obj[1:-1], safe=False)
   chatMessages = Message.objects.filter(chat__id=1) # Indenting is important here!
   return render(request, 'chat/index.html', {'messages': chatMessages})

def login_view(request):
   # redirect = request.GET.get('next')
   if request.method == 'POST':
      user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
      if user:
         login(request, user)
         # get a get variable (=in url) to redirect
         return HttpResponseRedirect('/chat/')
      else:
         return render(request, 'auth/login.html', {'wrongPassword':True})
   return render(request, 'auth/login.html')

def register_user(request):
   if request.method == 'POST':
       password1=request.POST['password1']
       password2=request.POST['password2']
       username=request.POST['username']
       email=request.POST['email']

       if password1==password2:
            if User.objects.filter(username=username).exists():
               return render(request, 'auth/register.html', {'userTaken': True})
            elif User.objects.filter(email=email).exists():
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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/register/')
