import datetime
import numpy as np
import plotly.graph_objs as go
from plotly.offline import plot
from . models import Measurement, Device

def measurements_plot(device_id):
    #filter data to specified device
    device_data = Measurement.objects.filter(device_id_id = int(device_id))
    
    #filter data to each attribute 
    attributes_list = ['temperature','humidity','light']
    datetime = device_data.values_list('datetime', flat = True)
    plots = []
    for attribute in attributes_list:
        name = attribute
        attribute = device_data.values_list(attribute, flat = True)
        plot_view = go.Scatter(
                x = list(datetime),
                y = list(attribute),
                name = name
                )
        plots.append(plot_view)

    layout = go.Layout(
        xaxis = dict(autorange=True),
        yaxis = dict(autorange=True)
        )

    figure = go.Figure(data = plots, layout = layout)
    config = {'responsive': True}
    plot_div = plot(figure, output_type = 'div', config = config)
    return plot_div

def comparing_plot(attribute):
    #getting all devices id and names
    devices_id = list(Device.objects.values_list('id', flat = True))
    devices_name = list(Device.objects.values_list('name', flat = True))

    #store all devices data for specified attribute
    devices_attribute_data = []
    devices_attribute_data_datetime = []

    #filtering devices data with attribute
    device_data = []
    device_datetime = []
    for device in devices_id:
        device_data = Measurement.objects.filter(device_id_id = int(device))
        device_data = device_data.values_list(attribute.lower(), flat = True)
        data_datetime = device_data.values_list('datetime', flat = True)
        devices_attribute_data.append(device_data)
        devices_attribute_data_datetime.append(data_datetime)

    #gathering device data to one figure
    plots = []
    for dev_id in devices_id:
        plot_view = go.Scatter(
                y = list(devices_attribute_data[int(dev_id)-1]),
                x = list(devices_attribute_data_datetime[int(dev_id)-1]),
                name = devices_name[int(dev_id)-1]
                )
        plots.append(plot_view)

    layout = go.Layout(
        xaxis = dict(autorange=True),
        yaxis = dict(autorange=True)
        )

    figure = go.Figure(data = plots, layout = layout)
    config = {'responsive': True }
    plot_div = plot(figure, output_type = 'div', config = config)
    return plot_div
