from django.db import models
from utilities.querysets import RestrictedQuerySet


class EquipmentData(models.Model):
    region = models.ForeignKey(
        to='dcim.Region',
        related_name='region_set',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    city = models.ForeignKey(
        to='dcim.Region',
        related_name='city_set',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    site = models.ForeignKey(
        to='dcim.Site',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    device = models.ForeignKey(
        to='dcim.Device',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    manufacturer = models.ForeignKey(
        to='dcim.Manufacturer',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    model = models.ForeignKey(
        to='dcim.DeviceType',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    ip = models.ForeignKey(
        to='ipam.IPAddress',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    serial = models.CharField(
        max_length=400,
        blank=True,
        null=True
    )

    model_fact = models.CharField(
        max_length=400,
        blank=True,
        null=True
    )

    serial_fact = models.CharField(
        max_length=400,
        blank=True,
        null=True
    )

    date_create = models.DateTimeField(auto_now_add=True)

    error = models.TextField(
        max_length=500,
        blank=True,
        null=True
    )

    objects = RestrictedQuerySet.as_manager()

    def __str__(self):
        return f'{self.device}'

    class Meta:
        verbose_name_plural = 'Инвентаризация'
