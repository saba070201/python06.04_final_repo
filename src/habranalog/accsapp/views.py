from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from articleapp.models import * 

def signup(request):
    if request.user.is_authenticated:
      return redirect('articleapp:home')
    else:
      if request.method=='GET':
        return render(request,'accsapp/signup.html',{'form':UserCreationForm()})
      else:
        if request.POST['password1']==request.POST['password2']:
            try:
                user=User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('articleapp:home')
            except IntegrityError:
                return render(request,'accsapp/signup.html',{'form':UserCreationForm(),'error':'такой пользователь уже существует'})
        else:
            return render(request,'accsapp/signup.html',{'form':UserCreationForm(),'error':'пароли не совпадают'})
        

def signin(request):
    if request.user.is_authenticated:
       return redirect('articleapp:home')
    else:
      if request.method=='GET':
        return render(request,'accsapp/signin.html',{'form':AuthenticationForm()})
      else:
        user=authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
          return render(request,'accsapp/signin.html',{'form':AuthenticationForm(),'error':'такого пользователя не существует'})
        else:
          login(request,user)
          return redirect('articleapp:home')
  
      

@login_required
def signout(request):
  
    logout(request)
    return redirect('articleapp:home') 


@login_required 
def profile(request):
  publicart=Article.objects.filter(author=request.user,published=True)
  privateart=Article.objects.filter(author=request.user,published=False)
  return render(request,'accsapp/profile.html',context={'publicart':publicart,'privateart':privateart})