from django import forms
from utilities.forms import DynamicModelChoiceField
from extras.forms import CustomFieldModelFilterForm

from dcim.models import Device, Site, Region, Manufacturer, DeviceType
from ipam.models import IPAddress

from .models import EquipmentData


class EquipmentDataFilterForm(CustomFieldModelFilterForm):
    model = EquipmentData
    region = DynamicModelChoiceField(
        queryset=Region.objects.filter(level=0),
        required=False
    )
    city = DynamicModelChoiceField(
        queryset=Region.objects.filter(level=1),
        required=False
    )
    site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        required=False
    )
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False
    )
    manufacturer = DynamicModelChoiceField(
        queryset=Manufacturer.objects.all(),
        required=False
    )
    model_device = DynamicModelChoiceField(
        queryset=DeviceType.objects.all(),
        required=False
    )
    ip = DynamicModelChoiceField(
        queryset=IPAddress.objects.all(),
        required=False
    )
