from django.contrib import admin
from .models import Product,User,Company,Enquiry,Fantype

# Register your models here.
admin.site.register(Company)
admin.site.register(Product)
# admin.site.register(User)
admin.site.register(Enquiry)
admin.site.register(Fantype)