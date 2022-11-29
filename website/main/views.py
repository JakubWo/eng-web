import json

from django.http import HttpResponse, JsonResponse
# from django.template.library im
from django.template.defaultfilters import register
from django.views.generic import TemplateView
from requests import get
from typing import Dict

from .models import load_charts_data, load_single_chart_data


@register.filter(name='get_list_elem')
def get_list_elem(value, arg):
    for plot in value:
        if plot['name'] == arg:
            return plot

    return None


class MainView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs) -> Dict[str, any]:
        context = super().get_context_data(**kwargs)
        data = get('https://144.24.161.226/getMeasurements?format=json&last=100', verify=False)
        plots = load_charts_data(json.loads(data.text))
        context['plots'] = list()

        for key in plots:
            context['plots'].append(plots[key].get_records())

        return context


class PlotView(TemplateView):
    template_name = 'plot/index.html'

    # plot_name = variable
    def get_context_data(self, **kwargs) -> Dict[str, any]:
        context = super().get_context_data(**kwargs)
        data = get('https://144.24.161.226/getMeasurements?format=json', verify=False)
        plots = load_single_chart_data(json.loads(data.text), context['plot_name'])
        context['plots'] = list()

        for key in plots:
            context['plots'].append(plots[key].get_records())

        return context
