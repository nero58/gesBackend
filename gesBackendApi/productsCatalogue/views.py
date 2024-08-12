from rest_framework.views import APIView
from rest_framework import status
from fuzzywuzzy import fuzz, process
from .models import Product
from .filters import ProductFilter
from rest_framework import generics
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import AllProductSerializer,CompaniesRouteSerializer,ManufacturerSerializer,SingleProductSerializer,SearchProductSerializer
from productsCatalogue.models import Product,Company,User


def getroutes(request):
    routes=[
        {"GET":"api/products/all"},
        {"GET":"api/product/<part_number>"},
        {"GET":"api/companies/all"},
        {"GET":"api/products/<company_name>"},
        {"GET":"api/products/search/?query=<str>"},
        ]

    return JsonResponse(routes,safe=False)

@api_view(['GET'])
def getAllProducts(request):
    pro = Product.objects.all()
    serial = AllProductSerializer(pro, many=True)

    return Response(serial.data)

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
    compserial = ManufacturerSerializer(comp, many=True)
    return Response(compserial.data)


class ProductSearchView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = SearchProductSerializer
    filterset_class = ProductFilter
