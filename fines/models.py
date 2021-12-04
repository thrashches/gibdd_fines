from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Driver(models.Model):
    class Meta:
        verbose_name = 'водитель'
        verbose_name_plural = 'водители'

    full_name = models.CharField(max_length=255, verbose_name='ФИО')

    def __str__(self):
        return f'{self.full_name}'


class Fine(models.Model):
    class Meta:
        verbose_name = 'штраф'
        verbose_name_plural = 'штрафы'
        ordering = ['-fine_date']

    accident_number = models.CharField(max_length=25, unique=True, verbose_name='номер постановления')
    price = models.IntegerField(blank=True, null=True, verbose_name='сумма штрафа')
    accident_date = models.DateField(blank=True, null=True, verbose_name='дата нарушения')
    accident_time = models.TimeField(blank=True, null=True, verbose_name='время нарушения')
    fine_date = models.DateField(blank=True, null=True, verbose_name='дата вынесения постановления')
    car = models.ForeignKey('Car', related_name='fines', null=True, blank=True, on_delete=models.CASCADE, verbose_name='автомобиль')
    pay_status = models.BooleanField(default=False, verbose_name='статус оплаты')

    def __str__(self):
        return f'{self.accident_number}'


class Car(models.Model):
    class Meta:
        verbose_name = 'автомобиль'
        verbose_name_plural = 'автомобили'

    auto_id = models.IntegerField(unique=True, verbose_name='id автомобиля в API')
    auto_number = models.CharField(max_length=10, blank=True, null=True, verbose_name='гос номер(без региона)')
    auto_region = models.CharField(max_length=3, blank=True, null=True, verbose_name='регион')
    auto_cdi = models.CharField(max_length=10, blank=True, null=True, verbose_name='номер стс')
    auto_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='название автомобиля')

    def __str__(self):
        return f'{self.auto_id}: {self.auto_number}{self.auto_region}'


class Profile(AbstractUser):
    pass
