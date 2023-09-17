from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai

from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat
from django.utils import timezone
# Create your views here.


openai_api_key = 'ENTER YOUR SECRET API KEY FROM OPEN AI HERE '
openai.api_key = openai_api_key
content = """
        Answer as a assistant 
    
    """
messages = [ {"role": "system", "content":
              content} ]



def ask_openai(message):
    
    
    messages.append(
            {"role": "user", "content": message},
        )
    chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )

    reply = chat.choices[0].message.content
    return reply

def chatbot(request):
    if request.user.is_authenticated:
        chats = Chat.objects.filter(user=request.user)
        if request.method == 'POST':
            
        
            message = request.POST.get('message')
            response =  ask_openai(message)
            
            chat = Chat(user=request.user, message= message, response = response, created_at = timezone.now() )
            chat.save()
            return JsonResponse({'message': message, 'response': response})
        return render(request, 'chatbot.html', {'chats':chats})
    else:
        return render(request, 'chatbot.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        pw1 = request.POST['password1']
        pw2 = request.POST['password2']
        
        if pw1 == pw2:
            try:
                user = User.objects.create_user(username,email,pw1)
                user.save()
                auth.login(request, user)
                return redirect('login')
                pass
            except:
                 error_message = 'Could not create account'
            return render(request, 'register.html', {'error_message':error_message})
                
        else:
            error_message = 'Password dont match'
            return render(request, 'register.html', {'error_message':error_message})
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

def delete(request):
    if request.user.is_authenticated:
        chats = Chat.objects.filter(user=request.user)
        chats.delete()
    return redirect('chatbot')
    
    
    
