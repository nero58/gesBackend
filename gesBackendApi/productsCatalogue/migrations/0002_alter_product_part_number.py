# Generated by Django 4.2.14 on 2024-07-30 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productsCatalogue', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='part_number',
            field=models.CharField(blank=True, max_length=20, unique=True),
        ),
    ]
