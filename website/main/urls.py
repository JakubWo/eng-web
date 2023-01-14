from django.urls import path
from .views import MainView
from .views import PlotView
from .views import get_last_measurement

urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('plot/<str:plot_name>', PlotView.as_view(), name='plot'),
    path('ajax/last-measurement', get_last_measurement, name='last_measurement')
]
