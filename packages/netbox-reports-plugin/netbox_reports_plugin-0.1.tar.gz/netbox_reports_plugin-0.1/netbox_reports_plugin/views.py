from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import EquipmentData
import xlsxwriter
from netbox.views import generic
from io import BytesIO
from django.http import StreamingHttpResponse
from .tables import EquipmentDataTable
from django.db import connection
from .filters import EquipmentDataFilterSet
from .forms import EquipmentDataFilterForm


class ReportsDeviceListView(generic.ObjectListView):
    queryset = EquipmentData.objects.all().select_related('region').select_related('device').select_related(
        'site').select_related('ip').select_related('manufacturer').select_related('model')
    table = EquipmentDataTable
    template_name = "netbox_reports_plugin/reports_device_list.html"
    filterset = EquipmentDataFilterSet
    filterset_form = EquipmentDataFilterForm


def download_file(request):
    try:
        output = BytesIO()
        book = xlsxwriter.Workbook(output)
        sheet = book.add_worksheet()

        """Формируем заголовки из полей модели"""
        headlines = list(map(lambda x: x.verbose_name, EquipmentData._meta.get_fields()))[1:]

        """sheet.write(row, column, cell_data)"""
        dict_headlines = {}
        for column, cell_data in enumerate(headlines):
            dict_headlines[cell_data] = column
            sheet.write(0, column, cell_data)

        """Получаем данные об устройствах"""
        data = EquipmentData.objects.all().values(
            'region__name',
            'city__name',
            'site__name',
            'device__name',
            'manufacturer__name',
            'model__model',
            'ip__address',
            'serial',
            'model_fact',
            'serial_fact',
            'date_create',
            'error'
        )

        for row, data_dict in enumerate(data, start=1):
            for column, value in enumerate(data_dict.values()):
                sheet.write(row, column, str(value))

        book.close()
        output.seek(0)  # seek stream on begin to retrieve all data from it

        # send "output" object to stream with mimetype and filename
        response = StreamingHttpResponse(
            output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=reports_device.xlsx'
        return response
    except Exception as e:
        return HttpResponse('<h1>error</h1>')
