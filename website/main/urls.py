from django.urls import path
from .views import MainView
from .views import ArchiveView
from .views import PlotView
from .views import get_last_measurement
from .views import download_csv

urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('archive', ArchiveView.as_view(), name='archive'),
    path('plot/<str:plot_name>', PlotView.as_view(), name='plot'),
    path('ajax/last-measurement', get_last_measurement, name='last_measurement'),
    path('ajax/download/<str:plot_name>', download_csv, name='download_csv')
]
