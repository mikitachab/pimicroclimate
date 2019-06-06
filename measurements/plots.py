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
    plot_div = plot(fig, output_type = 'div', config = config)
    return plot_div

def comparing_plot(attribute):
    #getting all devices id
    devices_id = list(Device.objects.values_list('id', flat = True))
    #store all devices data for specified attribute
    devices_attribute_data = []
    devices_attribute_data_datetime = []
    device_data = []
    device_datetime = []
    #filtering devices data with attribute
    device_data = []
    data_datetime = []
    for device in devices_id:
        device_data = Measurement.objects.filter(device_id_id = int(device))
        device_data = device_data.values_list(attribute.lower(), flat = True)
        data_datetime = device_data.values_list('datetime', flat = True)
        devices_attribute_data.append(device_data)
        devices_attribute_data_datetime.append(data_datetime)

    plots = []
    for dev_id in devices_id:
        view = go.Scatter(
                y = list(devices_attribute_data[int(dev_id)-1]),
                x = list(devices_attribute_data_datetime[int(dev_id)-1]),
                name = 'Device id: '+str(dev_id)
                )
        plots.append(view)
    layout = go.Layout(
        xaxis = dict(
            autorange=True
        ),
        yaxis = dict(
            autorange=True
        )
    )
    fig = go.Figure(data = plots, layout = layout)
    config = {'responsive': True }
    plot_div = plot(fig, output_type = 'div', config = config)
    return plot_div
