from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.getroutes),
    path("api/products/all", views.getAllProducts), #ALL PRODUCTS
    path("api/product/<str:partnumber>", views.getProduct), #ONE PRODUCT USING ID
    path("api/companies/all", views.getCompanies), #ALL COMPANIES
    path("api/companies/<str:company>", views.getCompanyAndProducts), #ALL PRODUCTS OF A COMPANY_NAME
    # path("product/<", views.getCompanies), #A PRODUCT OF A COMPANY
    # path("products/<str:company>", views.getCompanyProducts), #ALL PRODUCTS USING COMPANY NAME
    # path("companies/<", views.getCompanies),

    # path("submit-enquiry/", views.postEnquiry), #POST REQ , UPLOAD PHOTO, SAVE DETAILS IN ENQUIRY TABLE


]