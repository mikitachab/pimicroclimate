import json
from django.shortcuts import render
from rest_framework import viewsets
from . models import Measurement
from . models import Device
from .serializers import MeasurementSerializer
from django.http import HttpResponse
from . import plots
from django.core.paginator import Paginator


def table(request):
    devices = Device.objects.all().order_by('id')
    if request.method == 'POST':
        try:
            device_id = request.session['dev_id']
            if int(device_id) > 0:
                print("DEVICE ID: ", device_id)
                data = request.POST.get('dev')
                queryset = Measurement.objects.filter(device_id_id=int(data))
                print(queryset)
                #need to continue
        except KeyError:
            print("No such attribute")

    request.session['dev_id'] = '1'
    queryset = Measurement.objects.all().order_by('id')
    paginator = Paginator(queryset, 30)
    page = request.GET.get('page')
    queryset = paginator.get_page(page)
    context = {
            "data_list": queryset,
            "index" : "/",
            "title": "Measured data",
            "devices": devices
        }
    return render(request, "table.html", context)

def plot(request):
    queryset = Measurement.objects.all().order_by('id')
    plot = plots.measurements_plot()
    context = {
        "title": "Measurements plot",
        "index" : "/",
        "plot": plot
    }
    return render(request, "plot.html", context)


class MeasurementView(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
