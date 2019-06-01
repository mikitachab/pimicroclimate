from django.contrib import admin
from .models import Measurement, Device

admin.site.register(Measurement)
admin.site.register(Device)
