import datetime
import numpy as np
import plotly.graph_objs as go
from plotly.offline import plot
from . models import Measurement


def measurements_plot(device_id):
    #filter data to specified device
    datetime = Measurement.objects.filter(device_id_id = int(device_id))
    temperature = Measurement.objects.filter(device_id_id = int(device_id))
    humidity = Measurement.objects.filter(device_id_id = int(device_id))
    light = Measurement.objects.filter(device_id_id = int(device_id))
    #apply columns data
    datetime = datetime.values_list('datetime', flat = True)
    temperature = temperature.values_list('temperature', flat = True)
    humidity = humidity.values_list('humidity', flat = True)
    light = light.values_list('light', flat = True)
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
