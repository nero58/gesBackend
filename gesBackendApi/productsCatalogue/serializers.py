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
        fields = ['company_name','about','products']
    
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

class AllProductSerializer(serializers.ModelSerializer):

    manufacturer = ManufacturerSerializer()
    img = ProductImageSerializer(many=True, source='images')
    details = serializers.SerializerMethodField()
    # related = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'img', 'manufacturer', 'details']

    def get_details(self, obj):
        return [
            {'part_number': obj.part_number},
            {'ac_dc': obj.ac_dc},
            {'fan_type': FanTypeSerializer(obj.fan_type).data},
            {'size': f"{obj.length} MM x {obj.width} MM x {obj.height} MM"},
            {'voltage': f"{obj.voltage} VDC"},
            {'current': f"{obj.current} A"},
            {'termination': f"{obj.termination} Wires" if int(obj.termination) > 1 else f"{obj.termination} Wire"},
            {'instock': obj.instock}
        ]


class RelatedProductSerializer(serializers.ModelSerializer):
    img = ProductImageSerializer(many=True, source='images')

    class Meta:
        model = Product
        fields = ['part_number', 'img']

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
