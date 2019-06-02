import json
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context = {
            "title" : "Welcome on PiMicolimate",
            "data_table" : "/table/data",
            "data_view" : "/table/view"
        }
    return render(request, "index.html", context)
