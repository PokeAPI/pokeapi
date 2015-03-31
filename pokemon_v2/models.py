from __future__ import unicode_literals
from django.db import models

class Ability(models.Model):

	id = models.IntegerField()

	name = models.CharField(max_length=30)

	generation =  models.IntegerField()

	is_main_series = models.IntegerField()



class EggGroups(models.Model):

	id = models.IntegerField()

	name = models.CharField(max_length=30)



class Gender(model.Models):

	id = models.IntegerField()

	name = models.CharField(max_length=12)



class Generation(models.Model):

	id = models.IntegerField()

	main_region_id = models.IntegerField()

	name = models.CharField(max_length=30)



class Move

	id = models.IntegerField()

	name = models.CharField(max_length=30)

	generaion_id = models.IntegerField()

	type_id = models.IntegerField()

	power = models.IntegerField()

	pp = models.IntegerField()

	accuracy = models.IntegerField()

	priority = models.IntegerField()

	target_id = models.IntegerField()

	damage_class_id = models.IntegerField()

	effect_id = models.IntegerField()

	effect_chance = models.IntegerField()

	contest_type_id = models.IntegerField()

	contest_effect_id = models.IntegerField()

	super_contest+effect_id = models.IntegerField()



class Nature(models.Model):

	id = models.IntegerField()

	name = CharField(max_length=30)

	decreased_stat_id = models.IntegerField()

	increased_stat_id = models.IntegerField()

	hates_flavor_id = models.IntegerField()

	likes_flavor_id = models.IntegerField()

	game_index = models.IntegerField()



class Pokedex(models.Model):

	id = models.IntegerField()

	region_id = models.IntegerField()

	name = models.CharField(max_length=30)

	is_main_series = models.IntegerField()



class Pokemon(models.Model):

	id = models.IntegerField()

	name = models.CharField(max_length=50)

	species_id = models.IntegerField()

	height = models.CharField(max_length=10)

    weight = models.CharField(max_length=10)

    base_experience = models.IntegerField()

    order = models.IntegerField()

    is_default = models.IntegerField()
