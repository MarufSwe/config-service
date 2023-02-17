from django.urls import path
from .views import *
from . import views


urlpatterns = [
    path('config', views.config_view, name='config-view'),

]
