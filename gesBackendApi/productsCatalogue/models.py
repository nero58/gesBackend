from django.db import models
from django.contrib.auth.models import User

#Signup signin ???? for admin access
class User(User):
    pass
    def __str__(self):
        return self.username

class Company(models.Model):
    company_name=models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.company_name
    
class Fantype(models.Model):
    type= models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.type

class Product(models.Model):
    manufacturer = models.ForeignKey(Company, on_delete=models.CASCADE)
    part_number=models.CharField(max_length=20,blank=True,unique=True)
    fan_type = models.ForeignKey(Fantype, on_delete=models.CASCADE)
    ac_dc = models.CharField(max_length=4,choices=[("AC","AC"),("DC","DC")])
    length = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    voltage = models.CharField(max_length=10)
    current = models.CharField(max_length=10)
    termination = models.CharField(max_length=10)
    instock = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.manufacturer} {self.part_number}" 
    
#POST 
class Enquiry(models.Model):
    full_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField() #Not required
    manufacturer= models.CharField(max_length=50)
    product_name = models.CharField(max_length=100)
    discription = models.CharField(max_length=200)
    # images = models.ImageField() #Not required


