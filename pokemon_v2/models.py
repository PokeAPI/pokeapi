from __future__ import unicode_literals
from django.db import models


class AbilityDescription(models.Model):

  ability_id = models.IntegerField()

  local_language_id = models.IntegerField()

  short_effect = models.CharField(max_length=200)

  effect = models.CharField(max_length=1000)


class AbilityFlavorText(models.Model):

  ability_id = models.IntegerField()

  version_group_id = models.IntegerField()

  language_id = models.IntegerField()

  flavor_text = models.CharField(max_length=100)


class AbilityName(models.Model):

  ability_id = models.IntegerField()

  local_language_id = models.IntegerField()

  name = models.CharField(max_length=30)

  def __str__(self):

        return self.name


class Ability(models.Model):

  flavor_text = models.ForeignKey(AbilityFlavorText, blank=True, null=True)

  generation =  models.IntegerField()

  is_main_series = models.IntegerField()

  description = models.OneToOneField(AbilityDescription, blank=True, null=True)

  name = models.CharField(max_length=30)

  names = models.ForeignKey(AbilityName, blank=True, null=True)
