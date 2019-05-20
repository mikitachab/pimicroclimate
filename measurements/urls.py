from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('measurements', views.MeasurementView)

urlpatterns = [
    path('', include(router.urls)),
    path('table/', views.table)
]
