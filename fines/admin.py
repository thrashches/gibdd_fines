import json

import requests

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path

from .models import Driver, Fine, Car, Profile
from django.contrib.auth.admin import UserAdmin
from django.conf import settings

# Register your models here.

admin.site.site_header = 'Штрафы'
admin.site.register(Driver)


# admin.site.register(Car)
# admin.site.register(Fine)

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'auto_name', 'fines_count']
    search_fields = ['auto_number', 'auto_id']
    list_filter = ['auto_name']
    change_list_template = 'update_cars.html'

    def fines_count(self, obj):
        return obj.fines.count()

    fines_count.short_description = 'штрафы'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("update/", self.update),
        ]
        return my_urls + urls

    def update(self, request):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {settings.API_KEY}'
        }
        url = 'https://api.onlinegibdd.ru/v3/partner_auto/'

        # 883878
        response = requests.post(headers=headers, url=url)
        data = response.json()
        # with open('autos.json', 'w') as f:
        #     json.dump(data, f)
        cars = data['data'].keys()
        for car_num in cars:
            car, created = Car.objects.get_or_create(auto_id=data['data'][car_num]['id'])
            car_dict = {
                'auto_number': data['data'][car_num]['auto_number'],
                'auto_region': data['data'][car_num]['auto_region'],
                'auto_cdi': data['data'][car_num]['auto_cdi'],
                'auto_name': data['data'][car_num]['auto_name']
            }
            Car.objects.filter(id=car.id).update(**car_dict)

        return HttpResponseRedirect("../")


@admin.register(Profile)
class ProfileAdmin(UserAdmin):
    pass


@admin.register(Fine)
class FineAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'car', 'pay_status']
    search_fields = ['accident_number']
    list_filter = ['car', 'pay_status']
    change_list_template = "update_fines.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("update/", self.update),
        ]
        return my_urls + urls

    def update(self, request):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {settings.API_KEY}'
        }
        params = {
            'status': 'all'
        }
        url = 'https://api.onlinegibdd.ru/v3/partner_fines/'

        # 883878
        response = requests.post(headers=headers, url=url, params=params)
        data = response.json()
        # with open('fines.json', 'w') as f:
        #     json.dump(data, f)

        cars = list(data['data']['auto_list'])
        for car in cars:
            print(car)
            car_dict = data['data']['auto_list'][car]
            car_obj = Car.objects.filter(auto_id=data['data']['auto_list'][car]['auto_id'])
            offenses = list(car_dict['offense_list'].keys())
            for offence in offenses:
                print(car_dict["offense_list"][offence])

                offense_dict = {
                    'accident_number': car_dict["offense_list"][offence]['bill_id'],
                    'price': int(float(car_dict["offense_list"][offence]['pay_bill_amount'])),

                }
                if car_obj.count():
                    offense_dict['car'] = car_obj[0]
                if car_dict["offense_list"][offence]['gis_status'] == 'payed':
                    offense_dict['pay_status'] = True
                else:
                    offense_dict['pay_status'] = False
                if car_dict["offense_list"][offence]["offense_date"]:
                    offense_dict['accident_date'] = car_dict["offense_list"][offence]["offense_date"]
                if car_dict["offense_list"][offence]["offense_time"]:
                    offense_dict['accident_time'] = car_dict["offense_list"][offence]["offense_time"]
                if car_dict["offense_list"][offence]["pay_bill_date"]:
                    offense_dict['fine_date'] = car_dict["offense_list"][offence]["pay_bill_date"]
                fine, created = Fine.objects.get_or_create(accident_number=offense_dict['accident_number'])
                Fine.objects.filter(id=fine.id).update(**offense_dict)

        # print(data)
        return HttpResponseRedirect("../")
