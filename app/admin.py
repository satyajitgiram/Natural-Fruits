from django.contrib import admin

# Register your models here.
from .models import FruitFarmingOption, Order

admin.site.register(FruitFarmingOption)
admin.site.register(Order)