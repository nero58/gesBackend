# Generated by Django 4.2.14 on 2024-08-07 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productsCatalogue', '0010_product_fan_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Color',
            field=models.CharField(default='Black', max_length=10),
        ),
        migrations.AddField(
            model_name='product',
            name='Material',
            field=models.CharField(default='Plastic', max_length=10),
        ),
        migrations.AddField(
            model_name='product',
            name='Warrenty',
            field=models.CharField(default='1 Year', max_length=10),
        ),
    ]
