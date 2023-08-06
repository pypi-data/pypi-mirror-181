from extras.filters import TagFilter
import django_filters
from django.db.models import Q

from ipam.models import IPAddress
from dcim.models import Device

from .models import EquipmentData


class EquipmentDataFilterSet(django_filters.FilterSet):
    class Meta:
        model = EquipmentData
        fields = ['region', 'city', 'site', 'device', 'manufacturer', 'model', 'ip']

    def search(self, queryset, name, value):
        """Perform the filtered search."""
        if not value.strip():
            return queryset
        qs_filter = (
                Q(id__icontains=value)
                | Q(number__icontains=value)
                | Q(description__icontains=value)
        )
        return queryset.filter(qs_filter)
