import datetime
import numpy as np
import plotly.graph_objs as go
from plotly.offline import plot
from . models import Measurement, Device

def measurements_plot(device_id):
    #filter data to specified device
    device_data = Measurement.objects.filter(device_id_id = int(device_id))
    #apply columns data
    datetime = device_data.values_list('datetime', flat = True)
    temperature = device_data.values_list('temperature', flat = True)
    humidity = device_data.values_list('humidity', flat = True)
    light = device_data.values_list('light', flat = True)
    temperature_plot = go.Scatter(
            x = list(datetime),
        y = list(temperature),
        name = 'temperature'
    )
    humidity_plot = go.Scatter(
            x = list(datetime),
        y = list(humidity),
        name = 'humidity'
    )
    light_plot = go.Scatter(
            x = list(datetime),
        y = list(light),
        name = 'light'
    )
    data = [temperature_plot, humidity_plot, light_plot]
    layout = go.Layout(
        xaxis = dict(
            autorange=True
        ),
        yaxis = dict(
            autorange=True
        )
    )
    fig = go.Figure(data = data, layout = layout)
    config = {'responsive': True}
    plot_div = plot(fig, output_type = 'div', config = config, include_plotlyjs = True)
    return plot_div

def comparing_plot(attribute):
    #getting all devices id
    devices = list(Device.objects.values_list('id', flat = True))
    print(devices)
    #filtering devices data with attribute
    device_data = []
    for device in devices:
    #    device_data.append(Measurements.objects.filter(device_id_id = int(device)).values_list(attribute, flat = True))
        print(device)
        device_data = Measurement.objects.filter(device_id_id = int(device))
        device_data = device_data.values_list(str(attribute), flat = True)
        print(device_data)
    return plot_div
