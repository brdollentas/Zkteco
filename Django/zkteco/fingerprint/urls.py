from django.urls import path
from . import views

app_name = 'fingerprint'
urlpatterns = [
    path('', views.index, name = 'index')
]

