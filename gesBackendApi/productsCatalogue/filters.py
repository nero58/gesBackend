import django_filters
from django.db.models import Q
from .models import Product

class ProductFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='filter_by_all_fields')

    class Meta:
        model = Product
        fields = []

    def filter_by_all_fields(self, queryset, name, value):
        keywords = value.split()
        q_objects = Q()
        for keyword in keywords:
            q_objects |= (
                Q(part_number__icontains=keyword) |
                Q(manufacturer__company_name__icontains=keyword) |
                Q(fan_type__type__icontains=keyword) |
                Q(voltage__icontains=keyword) |
                Q(current__icontains=keyword) |
                Q(ac_dc__icontains=keyword) |
                Q(termination__icontains=keyword) |
                Q(instock__icontains=keyword)
            )
        print(q_objects)
        check =  queryset.filter(q_objects)
        print(check)
        return check
