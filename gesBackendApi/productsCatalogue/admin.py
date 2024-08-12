from django.contrib import admin
from .models import Product,User,Company,Fantype,Product, ProductImage, CompanyImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

class ComapnyImageInline(admin.TabularInline):
    model = CompanyImage
    extra = 1

class CompanyAdmin(admin.ModelAdmin):
    inlines = [ComapnyImageInline]


admin.site.register(ProductImage)
admin.site.register(Product, ProductAdmin,)
admin.site.register(CompanyImage)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Fantype)