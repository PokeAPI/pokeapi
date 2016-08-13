from django.db import models


class Alert(models.Model):

    active = models.BooleanField()
    message = models.CharField(max_length=255)
