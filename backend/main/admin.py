from django.contrib import admin
from . import models


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("title", )



@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("title", "country")
    

@admin.register(models.School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ("title", "city")
