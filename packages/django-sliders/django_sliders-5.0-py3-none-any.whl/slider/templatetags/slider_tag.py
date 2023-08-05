import json

from slider.models import Slider
from django import  template
from django.core import serializers

from slider.serializers import SliderTemplate

register = template.Library()

@register.inclusion_tag('slider_list.html')
def render_slider():
    sliders = Slider.objects.all()
    serializers = SliderTemplate(sliders, many = True)
    print(json.loads(json.dumps(serializers.data)))
    return {
        # "sliders": list(sliders.values("id", "slider_img__url"))
        # "slider_data": json.loads(json.dumps(serializers.data))
    }
