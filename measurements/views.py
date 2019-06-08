import json
from django.shortcuts import render
from rest_framework import viewsets
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from . serializers import MeasurementSerializer
from . import plots
from . models import Measurement
from . models import Device

#device from db. Global variable for methods
devices = Device.objects.all().order_by('id')

def temperature(request):
    temperature_range = []
    #apply new value in post request

    if request.method == 'POST':
        try:
            session_dev_id = request.session.get('dev_id')
            temperature_range.append(int(request.POST.get('temp_from')))
            temperature_range.append(int(request.POST.get('temp_to')))
            temperature_range = sorted(temperature_range)
            queryset = Measurement.objects.filter(device_id_id=int(session_dev_id)).order_by('id')
            queryset = queryset.filter(temperature__gt=temperature_range[0])
            queryset = queryset.filter(temperature__lt=temperature_range[1])
            paginator = Paginator(queryset, 30)
            page = request.GET.get('page')
            queryset = paginator.get_page(page)
            context = {
                    "title": "Measured data",
                    "data_list": queryset,
                    "plot" : "/data/plot/",
                    "index" : "/",
                    "devices": devices
                }
            return render(request, "table.html", context)
        except KeyError:
            print("No such attribute. view.table POST method Error.")
    return HttpResponseRedirect('/data/table/')



def table(request):
    #default attribute value if not presented
    session_dev_id = request.session.get('dev_id','1')

    filtered = False
    temperature_range = []
    #apply new value in post request
    if request.method == 'POST':
        try:
            request.session['dev_id'] = request.POST.get('dev')
            return HttpResponseRedirect('/data/table/')
        except KeyError:
            print("No such attribute. view.table POST method Error.")
            
    queryset = Measurement.objects.filter(device_id_id=int(session_dev_id)).order_by('id')
    paginator = Paginator(queryset, 30)
    page = request.GET.get('page')
    queryset = paginator.get_page(page)
    context = {
            "title": "Measured data",
            "data_list": queryset,
            "plot" : "/data/plot/",
            "index" : "/",
            "devices": devices
        }
    return render(request, "table.html", context)

def plot(request):
    session_dev_id = request.session.get('dev_id','1')
    if request.method == 'POST':
        try:
            request.session['dev_id'] = request.POST.get('dev')
            return HttpResponseRedirect('/data/plot/')
        except KeyError:
            print("No such attribute. view.plot POST method Error.")

    plot = plots.measurements_plot(session_dev_id)
    context = {
        "title": "Measurements plot",
        "table" : "/data/table/",
        "index" : "/",
        "devices" : devices,
        "plot": plot
    }
    return render(request, "plot.html", context)

def compare_attribute(request):
    attributes = ['Humidity', 'Light', 'Temperature']
    if request.method == 'POST':
        attribute = request.POST.get('attribute')
        plot = plots.comparing_plot(attribute)
        context = {
            "title" : "Compare devices data attribute",
            "attributes" : attributes,
            "index" : "/",
            "plot": plot
        }
        return render(request, "compare.html", context)

    context = {
            "title" : "Compare devices data attribute",
            "attributes" : attributes,
            "index" : "/"
    }
    return render(request, "compare.html", context)

class MeasurementView(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
