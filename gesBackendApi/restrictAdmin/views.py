from django.shortcuts import render,HttpResponse
from django.contrib.auth import authenticate, login, logout
# from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.urls import reverse
from django.http import Http404
from django.http import JsonResponse
# from django.middleware.csrf import get_token
import json
from django.http import JsonResponse
from django.http import HttpResponseNotFound




@api_view(["GET","POST"])
def login_view(request):
    if request.method == "POST":

        try:
            # Parse JSON data from request body
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)

        if not username or not password:
            return JsonResponse({"error": "Username and password are required."}, status=400)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponse("Allowed")
            # return Response({"authentication":True})
        else:
            return HttpResponse("NOt Allowed")
            # return Response({"authentication":False})
    else:
        return HttpResponse("This is the login page. Please send a POST request to authenticate.")


def logout_view(request):
    logout(request)
    return Response({"logout":True})
    


class RestrictStaffToAdminMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        admin_index_url = reverse('admin:index')
        admin_login_url = reverse('admin:login')
        
        if request.path.startswith(admin_index_url) or request.path.startswith(admin_login_url):
            if request.user.is_authenticated:
                if not request.user.is_staff: 
                    return HttpResponse("You are not allowed to access this page.")  #Ask to add frontend view here
                    # return Http404
            else:
                return HttpResponse("You are not allowed to access this page.")
                # return Http404
        response = self.get_response(request)
        return response



class if404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if response.status_code == 404:
            return HttpResponseNotFound('Oops! The page you are looking for does not exist.')
            # return Http404
        return response

# def csrf_token_view(request):
#     return JsonResponse({'csrfToken': get_token(request)})