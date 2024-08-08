from productsCatalogue.models import Product,Company,Fantype,ProductImage
from rest_framework import serializers
import json

class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['company_name','about']


    
class CompaniesRouteSerializer(serializers.ModelSerializer):
    products=serializers.SerializerMethodField()
    class Meta:
        model = Company
        fields = ['company_name','about','products']
    
    def get_products(self,obj):
        comp = Company.objects.get(company_name =  obj.company_name)
        products= Product.objects.filter(manufacturer =comp)

        return [{'partnumber': product.part_number} for product in products]

class FanTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fantype
        fields = ['type']  


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['image']

    def get_image(self, obj):
        if obj.image:
            return f"/{obj.image.name}"
        return None

class AllProductSerializer(serializers.ModelSerializer):

    manufacturer = ManufacturerSerializer()
    img = ProductImageSerializer(many=True, source='images')
    # fantype = serializers.SerializerMethodField()
    details = serializers.SerializerMethodField()

    # related = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'img', 'manufacturer', 'details']

    def get_details(self, obj):
        return [
            {"name":"fan type","value":json.loads(json.dumps(FanTypeSerializer(obj.fan_type).data))["type"]},
            {"name":'part number', "value": obj.part_number},
            {"name":'ac dc', "value": f" {obj.ac_dc}"},
            {"name":'size', "value": f"{obj.length} MM x {obj.width} MM x {obj.height} MM"},
            {"name":'voltage', "value": f"{obj.voltage} VDC"},
            {"name":'current', "value": f"{obj.current} A"},
            {"name":'termination', "value": f"{obj.termination} Wires" if int(obj.termination) > 1 else f"{obj.termination} Wire"},
            {"name":'Material', "value":obj.Material},
            {"name":'Color', "value": obj.Color},
            {"name":'Warrenty', "value": obj.Warrenty},
            {"name":'instock', "value": obj.instock},

        ]
    



class RelatedProductSerializer(serializers.ModelSerializer):
    
    image = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ["name",'image']
    
    def get_image(self,obj):
        first_image = obj.images.first()
        if first_image:
            return ProductImageSerializer(first_image).data['image']
        return None
    
    def get_name(self,obj):
        return f"{obj.part_number} {obj.manufacturer} Cooling Fan"

class SingleProductSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    related = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['product', 'related']

    def get_product(self, obj):
        return AllProductSerializer(obj).data

    def get_related(self, obj):
        related_products = Product.objects.filter(manufacturer=obj.manufacturer).exclude(part_number=obj.part_number)
        return RelatedProductSerializer(related_products, many=True).data
