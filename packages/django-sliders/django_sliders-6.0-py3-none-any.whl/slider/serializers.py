from rest_framework import serializers

from slider.models import Slider


class SliderTemplate(serializers.ModelSerializer):
    slider_img_url = serializers.SerializerMethodField()

    def get_slider_img_url(self, obj):
        return obj.slider_img.url

    class Meta:
        model = Slider
        fields = "__all__"