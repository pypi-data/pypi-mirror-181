from .models import EquipmentData
import django_tables2 as tables

from utilities.tables import BaseTable


class EquipmentDataTable(BaseTable):
    id = tables.Column(
        linkify=False,
    )
    region = tables.LinkColumn()
    city = tables.LinkColumn()
    site = tables.LinkColumn()
    device = tables.LinkColumn()
    manufacturer = tables.LinkColumn()
    model = tables.LinkColumn()
    ip = tables.LinkColumn()
    serial = tables.Column(
        linkify=False,
    )
    model_fact = tables.Column(
        linkify=False,
    )
    serial_fact = tables.Column(
        linkify=False,
    )
    date_create = tables.Column(
        linkify=False,
    )
    error = tables.Column(
        linkify=False,
    )

    class Meta(BaseTable.Meta):
        model = EquipmentData
        fields = (
            'region', 'city', 'site', 'device', 'manufacturer',
            'model', 'ip', 'serial', 'model_fact',
            'serial_fact', 'date_create', 'error'
        )
        default_columns = (
            'region', 'city', 'site', 'device', 'manufacturer',
            'model', 'ip', 'serial', 'model_fact',
            'serial_fact', 'date_create', 'error'
        )
