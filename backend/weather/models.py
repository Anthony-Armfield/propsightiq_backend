from django.db import models

class WeatherReading(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    location  = models.CharField(max_length=100)
    temperature = models.FloatField()
    description = models.CharField(max_length=100)
