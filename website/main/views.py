import json

from django.template.defaultfilters import register
from django.views.generic import TemplateView
from requests import get
from typing import Dict

from .models import map_data_to_object


@register.filter(name='get_plot')
def get_plot(value: list, arg: str):
    for plot in value:
        if plot.get_name() == arg:
            return plot

    return None


class MainView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs) -> Dict[str, any]:
        context = super().get_context_data(**kwargs)

        data = get('https://144.24.161.226/getMeasurements?format=json&last=100', verify=False)

        context['plots'] = map_data_to_object(json.loads(data.text))

        return context


class PlotView(TemplateView):
    template_name = 'plot/index.html'

    def get_context_data(self, **kwargs) -> Dict[str, any]:
        context = super().get_context_data(**kwargs)

        data = get('https://144.24.161.226/getMeasurements?format=json&measurement_type='+context['plot_name'], verify=False)

        context['plots'] = map_data_to_object(json.loads(data.text))

        return context
