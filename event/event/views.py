from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib import messages
from . import views
from .models import Users
import requests
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

@csrf_exempt
def home(request):
    if request.method == "POST":
        username1 = request.POST['regno']
        pass1 = request.POST['pass']
        user = authenticate(username=username1,password=pass1)
        api_key = '2bdfd538151fa5e10f69e4210fa683fb'
        current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

        weather_data1 = fetch_weather_and_forecast('Chennai', api_key, current_weather_url)
        
        context = {
            'weather_data1': weather_data1,
        
        }

        if user is not None:
            print(user)
            login(request, user)
            # Redirect to a success page or homepage
            return render(request,"home.html",context)
        else:
                # Return an error message indicating invalid credentials
            error_message = "Invalid username or password."
            return render(request, 'login1.html', {'custom_message': error_message})
    
    elif request.method == "GET":
        api_key = '2bdfd538151fa5e10f69e4210fa683fb'
        current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

        weather_data1 = fetch_weather_and_forecast('Chennai', api_key, current_weather_url)
        
        context = {
            'weather_data1': weather_data1,
        
        }
        return render(request,"home.html",context)
        
    
    return render(request,"home.html")




def fetch_weather_and_forecast(city, api_key, current_weather_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()
    lat, lon = response['coord']['lat'], response['coord']['lon']


    weather_data = {
        'city': city,
        'temperature': round(response['main']['temp'] - 273.15, 2),
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
    }


    return weather_data



def register(request):
    
    return render(request,"register.html")

def login1(request):
    if request.method == "POST":
        
        email12 = request.POST['emails']
        name12 = request.POST['username']
        password12 = request.POST['pass']
        myuser = User.objects.create_user(name12, email12, password12)
        myuser.save()
        message = request.POST.get('message', '')
        custom_message = f"Account Created Sucessfully"
        return render(request, 'login1.html', {'custom_message': custom_message})
        
    return render(request,"login1.html")

def event(request):

    if request.user.is_authenticated:

        user = User.objects.get(username=request.user.username)

        # Convert user data to a dictionary
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
        }
    

    send_mail(
        'Thank You for Registering',
        'Thank you for registering with us! We are excited to have you on board.Your registration is a crucial step in our journey together, and we are committed to providing you with a seamless and enjoyable experience. Whether you are here to learn, connect, or explore, we are here to support you every step of the way.',
        'caxzenofficial@gmail.com',
        [user_data['email']],
    )

    return render(request,"event.html")