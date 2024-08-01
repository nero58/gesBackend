from productsCatalogue.models import Product,Company,Fantype,User
from rest_framework import serializers

class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['company_name']

class FanTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fantype
        fields = ['type']  


class ProductSerializer(serializers.ModelSerializer):

    size = serializers.SerializerMethodField()
    voltage = serializers.SerializerMethodField()
    current = serializers.SerializerMethodField()
    termination = serializers.SerializerMethodField()
    manufacturer = ManufacturerSerializer()
    fan_type = FanTypeSerializer()

    class Meta:
        model = Product
        fields = ['id','manufacturer', 'part_number', 'ac_dc', 'fan_type','size', 'voltage', 'current', 'termination', 'instock']
        read_only_fields = ['id']

    def get_size(self, obj):
        return f"{obj.length} MM x {obj.width} MM x {obj.height} MM"

    def get_voltage(self, obj):
        return f"{obj.voltage} VDC"

    def get_current(self, obj):
        return f"{obj.current} A"
    
    def get_termination(self,obj):
        if(int(obj.termination)>1):
            return f'{obj.termination} Wires'
        return f'{obj.termination} Wire'
        
    
