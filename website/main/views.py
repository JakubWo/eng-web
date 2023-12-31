import csv
import json
import time

from django.http import JsonResponse
from django.http import HttpResponse
from django.template.defaultfilters import register
from django.views.generic import TemplateView
from requests import get
from typing import Dict
from datetime import datetime

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


def get_last_measurement(request) -> JsonResponse:
    if request.method != 'GET':
        return JsonResponse({'error': 'Unsupported request method'})

    data = get('http://eng_api_nginx/measurement/get?last=1')

    return JsonResponse(json.loads(data.text))


def download_csv(request, plot_name):
    filename = 'weather-station_' + plot_name + '_' + str(datetime.now().strftime('%d-%m-%Y_%H-%M-%S')) + '.csv'
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="' + filename + '"'},
    )

    url_params = ''
    if plot_name != 'all_data':
        url_params = '?measurement_type=' + plot_name

    data = get('http://eng_api_nginx/measurement/get' + url_params)
    data = json.loads(data.text)
    writer = csv.writer(response)

    if plot_name == 'all_data':
        csv_data = dict()
        title_row = ['timestamp']
        for key in data:
            title_row.append(key)
            for record in data[key]['measurements']:
                if record['timestamp'] not in csv_data:
                    csv_data[record['timestamp']] = []
                    csv_data[record['timestamp']].append(record['timestamp'])

                csv_data[record['timestamp']].append(record['value'])

        writer.writerow(title_row)

        for key in csv_data:
            writer.writerow(csv_data[key])

    else:
        writer.writerow(['timestamp', plot_name])
        for record in data[plot_name]['measurements']:
            writer.writerow([record['timestamp'], record['value']])

    return response


class ArchiveView(TemplateView):
    template_name = 'archive/index.html'

    def get_context_data(self, **kwargs) -> Dict[str, any]:
        context = super().get_context_data(**kwargs)

        data = get('http://eng_api_nginx/measurement/get?measurement_type=')

        context['plots'] = map_data_to_object(json.loads(data.text), 'limit')

        return context


class MainView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs) -> Dict[str, any]:
        context = super().get_context_data(**kwargs)

        data = get('http://eng_api_nginx/measurement/get?last=100')

        context['plots'] = map_data_to_object(json.loads(data.text), 'ostatnie 100 pomiarów')

        return context


class PlotView(TemplateView):
    template_name = 'plot/index.html'

    def get_context_data(self, **kwargs) -> Dict[str, any]:
        context = super().get_context_data(**kwargs)

        data = get('http://eng_api_nginx/measurement/get?measurement_type=' + context['plot_name'])

        context['plots'] = map_data_to_object(json.loads(data.text), 'cały okres')

        return context
