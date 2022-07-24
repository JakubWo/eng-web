import json

from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from requests import get
from typing import Dict

from .models import load_charts_data


class MainView(TemplateView):
    template_name = 'main/main.html'

    def get_context_data(self, **kwargs) -> Dict[str, any]:
        context = super().get_context_data(**kwargs)
        data = get('https://144.24.161.226/getMeasurements?format=json', verify=False)
        plots = load_charts_data(json.loads(data.text))
        context['plots'] = list()

        for key in plots:
            context['plots'].append(plots[key].get_records())

        return context
