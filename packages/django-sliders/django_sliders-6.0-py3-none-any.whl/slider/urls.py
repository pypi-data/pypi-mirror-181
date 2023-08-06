from django.urls import path

from . import views

app_name = 'slider'

urlpatterns = [
    path("", views.SliderIndex.as_view(), name="sliderIndex")
]