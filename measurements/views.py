import json
from django.shortcuts import render
from rest_framework import viewsets
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.db.models import Max
from . serializers import MeasurementSerializer
from . import plots
from . models import Measurement
from . models import Device

#device from db. Global variable for methods
devices = Device.objects.all().order_by('id')
filtered_queryset = []

def filter_by_attribute(request):
    session_dev_id = request.session.get('dev_id','1')
    #dictionary for data filtering
    attribute = {}
    #apply new values in post request
    if request.method == 'POST':
        try:
            session_dev_id = request.session.get('dev_id')
        except KeyError:
            print("No such attribute. view.temperature POST method Error.")

        #setting keywords for dictionary
        attribute_keyword = request.POST.get('filters').lower()
        attribute_from = attribute_keyword+'__gte'
        attribute_to = attribute_from.replace('__gte', '__lte')

        if not request.POST.get('temp_from','0'):
            attribute[attribute_from] = 0
        else:
            attribute[attribute_from] = int(request.POST.get('temp_from'))

        if not request.POST.get('temp_to','0'):
            attribute[attribute_to] = 0
        else:
            attribute[attribute_to] = int(request.POST.get('temp_to'))

        # simple filter 4 possibilities 
        # -> operator means after filler queryset
        # [0, 0] -> [0,max]
        # [0, X] -> [0, X+1]
        global filtered_queryset
        radio_button = request.POST.get('filter_radio_button')

        #trick for multiple filter
        if radio_button != 'OK':
            filtered_queryset = Measurement.objects.filter(device_id_id = int(session_dev_id))

        if attribute[attribute_from] == 0:
            if attribute[attribute_to] == 0:
                attribute[attribute_to] = list(filtered_queryset.aggregate(Max(attribute_keyword)).values())[0]
                filtered_queryset = filtered_queryset.filter(**attribute)
            else:
                filtered_queryset = filtered_queryset.filter(**attribute)
        else:
        # [X, 0] -> [X-1, max]
        # [A, B] -> [A-1, B+1]
            if attribute[attribute_to] == 0:
                attribute[attribute_to] = list(filtered_queryset.aggregate(Max(attribute_keyword)).values())[0]
                filtered_queryset = filtered_queryset.filter(**attribute)
            else:
                filtered_queryset = filtered_queryset.filter(**attribute)

        return HttpResponseRedirect('/data/table/')

    return HttpResponseRedirect('/data/table/')

def table(request):
    global filtered_queryset
    filters = ['Temperature', 'Humidity', 'Light']
    #default attribute value if not presented
    session_dev_id = request.session.get('dev_id','1')

    #apply new value in post request
    if request.method == 'POST':
        try:
            request.session['dev_id'] = request.POST.get('dev')
            filtered_queryset = []
            return HttpResponseRedirect('/data/table/')
        except KeyError:
            print("No such attribute. view.table POST method Error.")

    # applying filtered queryset
    if not filtered_queryset:
        queryset = Measurement.objects.filter(device_id_id=int(session_dev_id)).order_by('id')
    else:
        queryset = filtered_queryset.order_by('id')

    paginator = Paginator(queryset, 30)
    page = request.GET.get('page')
    queryset = paginator.get_page(page)
    context = {
            "title": "Measured data",
            "data_list": queryset,
            "plot" : "/data/plot/",
            "index" : "/",
            "filters" : filters,
            "devices": devices
        }
    return render(request, "table.html", context)

def plot(request):
    global filtered_queryset
    session_dev_id = request.session.get('dev_id','1')
    if request.method == 'POST':
        try:
            request.session['dev_id'] = request.POST.get('dev')
            filtered_queryset = []
            return HttpResponseRedirect('/data/plot/')
        except KeyError:
            print("No such attribute. view.plot POST method Error.")

    plot = plots.measurements_plot(session_dev_id, filtered_queryset)
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
