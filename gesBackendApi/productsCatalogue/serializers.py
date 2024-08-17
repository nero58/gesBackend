from productsCatalogue.models import Product, Company, Fantype, ProductImage, CompanyImage
from rest_framework import serializers
from django.core.cache import cache
from django.db.models import Prefetch, F, Value
from django.db.models.functions import Concat
from functools import wraps

def cache_result(timeout=3600):
    def decorator(func):
        @wraps(func)
        def wrapper(self, obj):
            # Use obj directly if it's a primitive type, otherwise use its id
            cache_key = f'{func.__name__}_{obj if isinstance(obj, (int, str)) else obj.id}'
            result = cache.get(cache_key)
            if result is None:
                result = func(self, obj)
                cache.set(cache_key, result, timeout)
            return result
        return wrapper
    return decorator

class CompanyImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = CompanyImage
        fields = ['image']

    def get_image(self, obj):
        return f"/{obj.image.name}" if obj.image else None

class ManufacturerSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()
    about = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['company_name', 'img', 'about']

    @cache_result()
    def get_img(self, obj):
        images = obj.images.all()
        return CompanyImageSerializer(images, many=True).data

    @cache_result()
    def get_about(self, obj):
        return [sentence for sentence in obj.about.split(". ") if sentence]

class CompaniesRouteSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    manufacturer = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['manufacturer', 'products']

    def get_manufacturer(self, obj):
        return ManufacturerSerializer(obj).data

    @cache_result()
    def get_products(self, obj):
        products = Product.objects.filter(manufacturer=obj).prefetch_related(
            Prefetch('productimages', queryset=ProductImage.objects.only('image'))
        )
        return RelatedProductSerializer(products, many=True).data

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
        return f"/{obj.image.name}" if obj.image else None

class AllProductSerializer(serializers.ModelSerializer):
    manufacturer = ManufacturerSerializer()
    img = serializers.SerializerMethodField()
    details = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'img', 'manufacturer', 'details']

    @cache_result()
    def get_details(self, obj):
        return [
            {"name": "fan type", "value": obj.fan_type.type},
            {"name": 'part number', "value": obj.part_number},
            {"name": 'ac dc', "value": f" {obj.ac_dc}"},
            {"name": 'size', "value": f"{obj.length} MM x {obj.width} MM x {obj.height} MM"},
            {"name": 'voltage', "value": f"{obj.voltage} VDC"},
            {"name": 'current', "value": f"{obj.current} A"},
            {"name": 'termination', "value": f"{obj.termination} Wires/Pins" if int(obj.termination) > 1 else f"{obj.termination} Wire/Pin"},
            {"name": 'Material', "value": obj.Material},
            {"name": 'Color', "value": obj.Color},
            {"name": 'Warrenty', "value": obj.Warrenty},
            {"name": 'RPM', "value": f"{obj.RPM}"},
            {"name": 'Airflow', "value": f"{obj.Airflow} CFM"},
            {"name": 'instock', "value": obj.instock},
        ]

    @cache_result()
    def get_img(self, obj):
        images = obj.productimages.all()
        return ProductImageSerializer(images, many=True).data

class RelatedProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["name", 'image']

    def get_image(self, obj):
        first_image = obj.productimages.first()
        return f"/{first_image.image.name}" if first_image else None

    def get_name(self, obj):
        return f"{obj.part_number} {obj.manufacturer} Cooling Fan"

class SingleProductSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    related = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['product', 'related']

    def get_product(self, obj):
        return AllProductSerializer(obj).data

    @cache_result()
    def get_related(self, obj):
        related_products = Product.objects.filter(manufacturer=obj.manufacturer).exclude(id=obj.id).prefetch_related(
            Prefetch('productimages', queryset=ProductImage.objects.only('image'))
        ).annotate(
            full_name=Concat(F('part_number'), Value(' '), F('manufacturer__company_name'), Value(' Cooling Fan'))
        ).values('id', 'full_name')[:5]
        
        return [{'name': product['full_name'], 'image': self.get_product_image(product['id'])} for product in related_products]

    @cache_result()
    def get_product_image(self, product_id):
        first_image = ProductImage.objects.filter(product_id=product_id).only('image').first()
        return f"/{first_image.image.name}" if first_image else None

class SearchProductSerializer(serializers.ModelSerializer):
    manufacturer = ManufacturerSerializer()
    details = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'manufacturer', 'details']

    @cache_result()
    def get_details(self, obj):
        return [
            {"name": "fan type", "value": obj.fan_type.type},
            {"name": 'part number', "value": obj.part_number},
            {"name": 'ac dc', "value": f" {obj.ac_dc}"},
            {"name": 'size', "value": f"{obj.length} MM x {obj.width} MM x {obj.height} MM"},
            {"name": 'voltage', "value": f"{obj.voltage} VDC"},
            {"name": 'current', "value": f"{obj.current} A"},
            {"name": 'termination', "value": f"{obj.termination} Wires/Pins" if int(obj.termination) > 1 else f"{obj.termination} Wire/Pin"},
            {"name": 'Material', "value": obj.Material},
            {"name": 'Color', "value": obj.Color},
            {"name": 'Warrenty', "value": obj.Warrenty},
            {"name": 'RPM', "value": f"{obj.RPM}"},
            {"name": 'Airflow', "value": f"{obj.Airflow} CFM"},
            {"name": 'instock', "value": obj.instock},
        ]