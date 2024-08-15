from django.db import models


# Create your models here.


class Destination(models.Model):
    place_name = models.CharField(max_length=100)
    weather = models.CharField(max_length=50)
    location_state = models.CharField(max_length=100)
    location_district = models.CharField(max_length=100)
    link = models.URLField(max_length=200)
    image = models.ImageField(upload_to='places/')
    description = models.CharField(max_length=5000)

    def __str__(self):
        return self.place_name
