from django.urls import path
from .views import MainView
from .views import PlotView

urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('/plots', PlotView.as_view(), name='plot')
]
