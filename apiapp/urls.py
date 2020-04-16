from django.urls import path
from .views import list_weather, update_location
from django.views.generic.base import TemplateView

urlpatterns = [
    # path('', views.index, name='index'),
    # path('', TemplateView.as_view(template_name='login.html'), name='login'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('weather/', list_weather, name='list_weather'),
    path('updatelocation/', update_location, name='update_location'),
]
