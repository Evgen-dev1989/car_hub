from django.shortcuts import render



from django.contrib.auth.models import User
from client.models import Client
from django.http import HttpResponse

def delete_all_users(request):

    Client.objects.all().delete()

    User.objects.all().delete()

    return HttpResponse("All users and clients have been deleted.")

def all_clients(request):

    clients = Client.objects.all()

    users = User.objects.all()
    
    return HttpResponse(context={'clients': clients, 'users': users})



