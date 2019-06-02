import json
from django.shortcuts import render
from rest_framework import viewsets
from .models import Measurement
from .serializers import MeasurementSerializer
from django.http import HttpResponse
from . import plots
from django.core.paginator import Paginator


def table(request):
    queryset = Measurement.objects.all().order_by('id')
    paginator = Paginator(queryset, 12)
    page = request.GET.get('page')
    queryset = paginator.get_page(page)
    plot = plots.measurements_plot()
    context = {
        "title": "Measurements",
        "data_list": queryset,
        "plot": plot
    }

    return render(request, "table.html", context)


class MeasurementView(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
