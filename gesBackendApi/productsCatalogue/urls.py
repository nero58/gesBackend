from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.getroutes),
    path("products/", views.getProducts), #ALL PRODUCTS
    path("products/<str:company>", views.getCompanyProducts), #ALL PRODUCTS USING COMPANY NAME
    path("product/<str:pk>", views.getProduct), #ONE PRODUCT USING ID
    path("submit-enquiry/", views.postEnquiry), #POST REQ , UPLOAD PHOTO, SAVE DETAILS IN ENQUIRY TABLE


]