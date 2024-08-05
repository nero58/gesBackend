from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import AllProductSerializer,CompaniesRouteSerializer,ManufacturerSerializer,SingleProductSerializer
from productsCatalogue.models import Product,Company,User


def getroutes(request):
    routes=[
        {"GET":"api/products/all"},
        {"GET":"api/product/<part_number>"},
        {"GET":"api/companies/all"},
        {"GET":"api/products/<company_name>"},
        # {"POST":"api/submit-enquiry"}
        ]

    return JsonResponse(routes,safe=False)

# @api_view(['GET'])
# def getCompanyProducts(request,company):
#     manufacturer = Company.objects.get(company_name=company)
#     pro = Product.objects.filter(manufacturer=manufacturer)
#     serial = ProductSerializer(pro, many=True)
#     return Response(serial.data)

@api_view(['GET'])
def getAllProducts(request):
    pro = Product.objects.all()
    serial = AllProductSerializer(pro, many=True)

    return Response(serial.data)
# Create your views here.

@api_view(["GET"])
def getProduct(request,part_number):
    pro = Product.objects.get(part_number=part_number)
    serial = SingleProductSerializer(pro,many=False) #FIX
    return Response(serial.data)

@api_view(["GET"])
def getCompanyAndProducts(request,company):
    comp = Company.objects.get(company_name=company)
    compserial = CompaniesRouteSerializer(comp,many=False)
    return Response(compserial.data)


@api_view(["GET"])
def getCompanies(request):
    comp = Company.objects.all()
    compserial = ManufacturerSerializer(comp,many=True)
    return Response(compserial.data)

# @api_view(["POST"])
# def postEnquiry(request):
    
#     pass