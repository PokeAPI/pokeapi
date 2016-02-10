from django.db import models

from datetime import date, timedelta


class ViewManager(models.Manager):

    def increment_view_count(self, version):

        view, _ = ResourceView.objects.get_or_create(
            version=version,
            date=date.today()
        )

        view.count = view.count + 1

        print view

        view.save()

    def total_count(self, version=0):

        if version:
            objects = ResourceView.objects.filter(version=version)
        else:
            objects = ResourceView.objects.all()

        t = 0
        for v in objects:
            t += v.count

        return t


class ResourceView(models.Model):

    objects = ViewManager()

    def __unicode__(self):
        return str(self.date) + ' - ' + str(self.count)

    count = models.IntegerField(max_length=1000, default=0)
    version = models.IntegerField(max_length=1, default=1)
    date = models.DateField(auto_now=True)

