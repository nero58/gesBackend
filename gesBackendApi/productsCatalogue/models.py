from django.db import models
from django.contrib.auth.models import User

def upload_to_company_image(instance, filename):
    comapny_name = instance.company_ref.company_name
    return f'companies/{comapny_name}/{filename}'

class CompanyImage(models.Model):
    company_ref = models.ForeignKey('Company', related_name='images', on_delete=models.CASCADE,null=True,blank=True)
    image = models.ImageField(upload_to=upload_to_company_image)

    def __str__(self):
        return f"Image for {self.company_ref}"
    

class Company(models.Model):
    company_name=models.CharField(max_length=50,unique=True)
    about = models.CharField(max_length=1000,blank=True)
    img = models.ManyToManyField(CompanyImage, blank=True, related_name='companies')
    
    def __str__(self):
        return self.company_name
    

    
class Fantype(models.Model):
    type= models.CharField(max_length=50)
    product = models.ForeignKey('Product', related_name='fantypes', on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.type

    
def upload_to_product_image(instance, filename):
    product_part_number = instance.product.part_number
    return f'products/{product_part_number}/{filename}'


class ProductImage(models.Model):
    product = models.ForeignKey('Product', related_name='productimages', on_delete=models.CASCADE,null=True,blank=True)
    image = models.ImageField(upload_to=upload_to_product_image)

    def __str__(self):
        return f"Image for {self.product.part_number}"
    
    
class Product(models.Model):
    img = models.ManyToManyField(ProductImage, blank=True, related_name='products')
    manufacturer = models.ForeignKey(Company, on_delete=models.CASCADE)
    part_number=models.CharField(max_length=20,blank=True,unique=True)
    fan_type = models.ForeignKey(Fantype,blank=True,on_delete=models.CASCADE,related_name="fantype",null=True)
    ac_dc = models.CharField(max_length=4,choices=[("AC","AC"),("DC","DC")])
    length = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    voltage = models.CharField(max_length=10)
    current = models.CharField(max_length=10)
    termination = models.CharField(max_length=10)
    Material = models.CharField(max_length=10, default="Plastic")
    Color = models.CharField(max_length=10, default="Black")
    Warrenty = models.CharField(max_length=10, default="1 Year")
    RPM = models.CharField(max_length=10, null=True, blank=True)
    Airflow = models.CharField(max_length=10, null=True, blank=True)
    instock = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.manufacturer} {self.part_number}" 
    



