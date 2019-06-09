import json
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context = {
            "title" : "Welcome on PiMicolimate",
            "data_table" : "/data/table",
            "data_plot" : "/data/plot",
            "compare" : "/data/compare"
        }
    return render(request, "index.html", context)
