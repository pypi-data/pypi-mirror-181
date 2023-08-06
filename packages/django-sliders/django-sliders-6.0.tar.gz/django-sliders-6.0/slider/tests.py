from django.test import TestCase

# Create your tests here.
from slider.models import Slider


class SliderTest(TestCase):
    fixtures = ["sliders.json"]

    def test_slider_total(self):
        sliders = Slider.objects.all()
        total = sliders.count()
        self.assertEqual(2, total)

