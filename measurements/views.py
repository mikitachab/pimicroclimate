import json
from django.shortcuts import render
from rest_framework import viewsets
from . models import Measurement
from . models import Device
from .serializers import MeasurementSerializer
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from . import plots
from django.core.paginator import Paginator


def table(request):
    devices = Device.objects.all().order_by('id')
    #default attribute value if not presented
    session_dev_id = request.session.get('dev_id','1')
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
    plot = plots.measurements_plot(session_dev_id)
    context = {
        "title": "Measurements plot",
        "table" : "/data/table/",
        "index" : "/",
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
