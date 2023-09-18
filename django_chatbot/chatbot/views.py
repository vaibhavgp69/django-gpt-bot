from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai

from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat
from django.utils import timezone
# Create your views here.


openai_api_key = 'Enter Your Api key'
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
    try:
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        reply = chat.choices[0].message.content
        print(reply)
        return reply
    except:
        reply = """
        Please enter your OPENAI API KEY in views.py file under chatbot folder to work
        ,   To find your API key : ask vaibhav or go to ur openai account and create one temporarily
        """
        return reply

    

def chatbot(request):
    if request.user.is_authenticated and request.user.username != 'anonymous':
        chats = Chat.objects.filter(user=request.user)
        if request.method == 'POST':
            
        
            message = request.POST.get('message')
            response =  ask_openai(message)
            # if  response ==None:
            #     reponse  = 'Please enter your openAI API key in views.py file'
            chat = Chat(user=request.user, message= message, response = response, created_at = timezone.now() )
            chat.save()
            return JsonResponse({'message': message, 'response': response})
        return render(request, 'chatbot.html', {'chats':chats})
    else:
        if request.method == 'POST':
            username = 'anonymous'
            email = 'none@gmail.com'
            pw1 = 'none'
            try:
                user_anon = User.objects.create_user(username,email,pw1)
                user_anon.save()
                message = request.POST.get('message')
                response =  ask_openai(message)
                # if  response ==None:
                #     reponse  = 'Please enter your openAI API key in views.py file'
                chat = Chat(user=user_anon, message= message, response = response, created_at = timezone.now() )
                chat.save()
                return JsonResponse({'message': message, 'response': response})
            except:
                user_anon = User.objects.get(username='anonymous')
                message = request.POST.get('message')
                response =  ask_openai(message)
                # if  response ==None:
                #     reponse  = 'Please enter your openAI API key in views.py file'
                chat = Chat(user=user_anon, message= message, response = response, created_at = timezone.now() )
                chat.save()
                return JsonResponse({'message': message, 'response': response})
                
        return render(request, 'chatbot.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            openai.api_key = request.user.last_name
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
        api_key = request.POST['last_name']
        openai.api_key = api_key
        if pw1 == pw2:
            try:
                
                if is_api_key_valid():   
                    user = User.objects.create_user(username,email,pw1,last_name=api_key)
                    user.save()
                    openai.api_key='none'
                    return redirect('login')
                else:
                    error_message = 'Invalid Api key '
                    
            except:
                 error_message = 'Could not create account'
            return render(request, 'register.html', {'error_message':error_message})
                
        else:
            error_message = 'Password dont match'
            return render(request, 'register.html', {'error_message':error_message})
    return render(request, 'register.html')

def logout(request):
    openai.api_key = 'none'
    auth.logout(request)
    return redirect('login')

def delete(request):
    if request.user.is_authenticated :
        chats = Chat.objects.filter(user=request.user)
        chats.delete()
    else :
        user_anon = User.objects.get(username='anonymous')
        chats = Chat.objects.filter(user=user_anon)
        chats.delete()
    return redirect('chatbot')

def is_api_key_valid():
    try:
        response = openai.Completion.create(
            engine="davinci",
            prompt="This is a test.",
            max_tokens=5
        )
    except:
        return False
    else:
        return True
    
    
    
