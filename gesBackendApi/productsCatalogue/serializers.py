from productsCatalogue.models import Product,Company,Fantype,ProductImage
from rest_framework import serializers

class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['company_name','img']


    
class CompaniesRouteSerializer(serializers.ModelSerializer):
    products=serializers.SerializerMethodField()
    class Meta:
        model = Company
        fields = ['company_name','img','about','products']
    
    def get_products(self,obj):
        comp = Company.objects.get(company_name =  obj.company_name)
        products= Product.objects.filter(manufacturer =comp)

        return [{'img':"img", 'partnumber': product.part_number} for product in products]

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

class ProductSerializer(serializers.ModelSerializer):

    manufacturer = ManufacturerSerializer()
    img = ProductImageSerializer(many=True, source='images')
    details = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'img', 'manufacturer', 'details']

    def get_details(self, obj):
        return DetailSerializer(obj, context=self.context).data
    
class DetailSerializer(serializers.ModelSerializer):
    
    size = serializers.SerializerMethodField()
    voltage = serializers.SerializerMethodField()
    current = serializers.SerializerMethodField()
    termination = serializers.SerializerMethodField()
    fan_type = FanTypeSerializer()

    class Meta:
        model = Product
        fields = ['part_number', 'ac_dc', 'fan_type', 'size', 'voltage', 'current', 'termination', 'instock']

    def get_size(self, obj):
        return f"{obj.length} MM x {obj.width} MM x {obj.height} MM"

    def get_voltage(self, obj):
        return f"{obj.voltage} VDC"

    def get_current(self, obj):
        return f"{obj.current} A"
    
    def get_termination(self, obj):
        if int(obj.termination) > 1:
            return f'{obj.termination} Wires'
        return f'{obj.termination} Wire'