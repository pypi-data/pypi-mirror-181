from django.contrib import admin

# Register your models here.
from slider.models import Slider

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    pass

