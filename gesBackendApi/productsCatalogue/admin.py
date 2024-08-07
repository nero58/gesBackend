from django.contrib import admin
from .models import Product,User,Company,Fantype,Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

admin.site.register(Product, ProductAdmin,)
admin.site.register(ProductImage)
admin.site.register(Company)
admin.site.register(Fantype)