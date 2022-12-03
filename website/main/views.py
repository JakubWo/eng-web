import json

from django.template.defaultfilters import register
from django.views.generic import TemplateView
from requests import get
from typing import Dict
import time

from .models import map_data_to_object, Plot


@register.filter(name='get_plot')
def get_plot_by_name(value: list, arg: str):
    for plot in value:
        if plot.get_name() == arg:
            return plot

    return None


@register.filter(name='get_last_week_plot')
def get_last_week_plot(value: Plot):
    records = list()
    timestamp = int((time.time() - 604800) * 1000)

    for record in value.get_records():
        if record['timestamp'] < timestamp:
            break
        records.append(record)

    return Plot(value.get_name(), records, 'ostatni tydzień')


@register.filter(name='get_last_month_plot')
def get_last_month_plot(value: Plot):
    records = list()
    timestamp = int((time.time() - 2629743) * 1000)

    for record in value.get_records():
        if record['timestamp'] < timestamp:
            break
        records.append(record)

    return Plot(value.get_name(), records, 'ostatni miesiąc')


class MainView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs) -> Dict[str, any]:
        context = super().get_context_data(**kwargs)

        data = get('https://144.24.161.226/getMeasurements?format=json&last=100', verify=False)

        context['plots'] = map_data_to_object(json.loads(data.text), 'ostatnie 100')

        return context


class PlotView(TemplateView):
    template_name = 'plot/index.html'

    def get_context_data(self, **kwargs) -> Dict[str, any]:
        context = super().get_context_data(**kwargs)

        data = get('https://144.24.161.226/getMeasurements?format=json&measurement_type='+context['plot_name'], verify=False)

        context['plots'] = map_data_to_object(json.loads(data.text), 'cały okres')

        return context
