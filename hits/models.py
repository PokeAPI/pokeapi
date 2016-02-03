from django.db import models

from datetime import date, timedelta


class ViewManager(models.Manager):

    def increment_view_count(self):

        view, _ = ResourceView.objects.get_or_create(
            date=date.today()
        )

        view.count = view.count + 1

        view.save()

    def total_count(self):

        t = 0
        for v in ResourceView.objects.all():
            t += v.count

        return t


class ResourceView(models.Model):

    objects = ViewManager()

    def __unicode__(self):
        return str(self.date) + ' - ' + str(self.count)

    count = models.IntegerField(max_length=1000, default=0)

    date = models.DateField(auto_now=True)
