from django.db import models

from datetime import date


class ResourceViewManager(models.Manager):

    def increment_view_count(self, version):

        view, _ = ResourceView.objects.get_or_create(
            version=version,
            date=date.today()
        )

        view.count = view.count + 1

        view.save()

    def total_count(self, version=0):

        all_hits = ResourceView.objects.all().values_list('count', flat=True)

        return sum(all_hits)


class ResourceView(models.Model):

    objects = ResourceViewManager()

    def __unicode__(self):
        return '{} - {}'.format(str(self.date), str(self.count))

    count = models.IntegerField(max_length=1000, default=0)
    version = models.IntegerField(max_length=1, default=1)
    date = models.DateField(auto_now=True)
