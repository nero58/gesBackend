from productsCatalogue.models import Product,Company,Fantype,ProductImage,CompanyImage
from rest_framework import serializers
import json


class CompanyImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = CompanyImage
        fields = ['image']

    def get_image(self, obj):
        if obj.image:
            return f"/{obj.image.name}"
        return None
    
class ManufacturerSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()
    about = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['company_name', 'img', 'about']

    def get_img(self, obj):
        images = obj.images.all() 
        return CompanyImageSerializer(images, many=True).data
    
    def get_about(self,obj):
        about = obj.about
        about_list = about.split(". ")
        return [sentence for sentence in about_list if sentence]

    

class CompaniesRouteSerializer(serializers.ModelSerializer):
    products=serializers.SerializerMethodField()
    manufacturer=serializers.SerializerMethodField()
    class Meta:
        model = Company
        fields = ['manufacturer','products']

    # def get_img(self, obj):
    #     images = obj.images.all() 
    #     return CompanyImageSerializer(images, many=True).data[0]["image"]

    def get_manufacturer(self,obj):
        return ManufacturerSerializer(obj).data

    
    def get_products(self,obj):
        comp = Company.objects.get(company_name =  obj)
        products= Product.objects.filter(manufacturer =comp)
        return RelatedProductSerializer(products,many=True).data

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
    img = serializers.SerializerMethodField()
    details = serializers.SerializerMethodField()

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
            {"name":'current', "value": f"{obj.current} A" },
            {"name":'termination', "value": f"{obj.termination} Wires/Pins" if int(obj.termination) > 1 else f"{obj.termination} Wire/Pin"},
            {"name":'Material', "value":obj.Material},
            {"name":'Color', "value": obj.Color},
            {"name":'Warrenty', "value": obj.Warrenty},
            {"name":'RPM', "value": f"{obj.RPM}"},
            {"name":'Airflow', "value": f"{obj.Airflow} CFM"},
            {"name":'instock', "value": obj.instock},

        ]
    def get_img(self, obj):
        images = obj.productimages.all() 
        return ProductImageSerializer(images, many=True).data

    



class RelatedProductSerializer(serializers.ModelSerializer):
    
    image = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ["name",'image']
    
    def get_image(self,obj):
        first_image = obj.productimages.first()
        if first_image:
            image = ProductImageSerializer(first_image, many=False)
            return image.data["image"]
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




class SearchProductSerializer(serializers.ModelSerializer):

    manufacturer = ManufacturerSerializer()
    img = serializers.SerializerMethodField()
    details = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'manufacturer', 'details']

    def get_details(self, obj):
        return [
            {"name":"fan type","value":json.loads(json.dumps(FanTypeSerializer(obj.fan_type).data))["type"]},
            {"name":'part number', "value": obj.part_number},
            {"name":'ac dc', "value": f" {obj.ac_dc}"},
            {"name":'size', "value": f"{obj.length} MM x {obj.width} MM x {obj.height} MM"},
            {"name":'voltage', "value": f"{obj.voltage} VDC"},
            {"name":'current', "value": f"{obj.current} A" },
            {"name":'termination', "value": f"{obj.termination} Wires/Pins" if int(obj.termination) > 1 else f"{obj.termination} Wire/Pin"},
            {"name":'Material', "value":obj.Material},
            {"name":'Color', "value": obj.Color},
            {"name":'Warrenty', "value": obj.Warrenty},
            {"name":'RPM', "value": f"{obj.RPM}"},
            {"name":'Airflow', "value": f"{obj.Airflow} CFM"},
            {"name":'instock', "value": obj.instock},

        ]