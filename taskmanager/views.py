from django.views.generic import UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from .forms import SignupForm, TaskForm
from .models import UserPic,UserInfo,Task

# Create your views here.
def signup_form_Page(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request,user)
            user = request.user
            UserPic.objects.create(user=user)
            return redirect('/')
    else:
        form = SignupForm()
    context = {'form':form}
    return render(request, 'registration_stuff/signup.html', context)

def log_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/')
    return render(request, 'registration_stuff/logout.html')

def log_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request,data=request.POST)
        if form.is_valid():
           username = form.cleaned_data['username']
           password = form.cleaned_data['password']
           user = authenticate(username=username, password=password)
           login(request,user)
           return redirect('/')
    else:
        form = AuthenticationForm()
    context = {'form':form}
    return render(request, 'registration_stuff/login.html', context)
@login_required(login_url='login')
def view_tasks(request):
    userdata = UserPic.objects.get(user=request.user)
    task = Task.objects.filter(user=request.user)
    print(task)
    context = {'userdata':userdata,'task':task}
    return render(request,'view_tasks.html',context)

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.user=request.user
            task = form.save()
            user = UserPic.objects.get(user=request.user)
            UserInfo.objects.create(user=user,task=task)
            return redirect('/')
    else:
        form = TaskForm()
    context = {'form':form}
    return render(request,'add_task.html',context)

def delete_all(request):
    tasks = Task.objects.filter(user=request.user)
    for task in tasks:
        task.delete()
    return redirect('/')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
            user = form.save()
            update_session_auth_hash(request, user)
            user_auth = authenticate(username=request.user.username,password=new_password)
            login(request,user_auth)
            messages.success(request,'Password had seccessfully changed you will receive an email')
            send_mail('Password change',f'your password had been changed your new password is {new_password}',settings.EMAIL_HOST_USER,[request.user.email]
                      ,fail_silently=True)
        else:
            messages.error(request,'An error happened and password had not change')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form':form}
    return render(request,'reset_password/change_password.html',context)

def deleteCompleted(request):
    Task.objects.filter(user=request.user,status__exact=True).delete()
    return redirect('/')

def completedTask(request, task_no)  :  
    task = Task.objects.get(task_no=task_no)
    task.status = True
    task.save()
    return redirect('/')

class Update_user(UpdateView):
    model = UserPic
    template_name = 'update_user.html'
    fields = ['profile_pic',]
    success_url = '/'
