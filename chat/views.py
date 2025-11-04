from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, password=password)
            return redirect('login')
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'home.html', {'users': users})

@login_required
def chat_view(request, username):
    receiver = User.objects.get(username=username)
    messages = Message.objects.filter(
        sender__in=[request.user, receiver],
        receiver__in=[request.user, receiver]
    ).order_by('timestamp')

    if request.method == 'POST':
        content = request.POST.get('message')
        if content:
            Message.objects.create(sender=request.user, receiver=receiver, content=content)
            return redirect('chat', username=receiver.username)

    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat.html', {
        'users': users,
        'receiver': receiver,
        'messages': messages
    })
