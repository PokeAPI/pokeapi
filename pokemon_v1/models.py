from __future__ import unicode_literals
from django.db import models

from imagekit.models.fields import ProcessedImageField
from imagekit.processors import ResizeToFill

from .utils import unique_filename


class DateTimeModel(models.Model):

    class Meta:
        abstract = True

    modified = models.DateTimeField(auto_now=True)

    created = models.DateTimeField(auto_now_add=True)


class Ability(DateTimeModel):

    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=50)

    description = models.TextField(max_length=200)


class Type(DateTimeModel):

    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=50)

    def _build_dict(self, items):
        lst = []
        for i in items:
            lst.append(dict(
                name=i.to.name,
                resource_uri='/api/v1/type/' + str(i.to.id) + '/'
            ))
        return lst

    def weakness_list(self):
        items = TypeChart.objects.filter(
            frm__name=self.name,
            ttype='weak')
        if items.exists():
            return self._build_dict(items)
        return []

    weaknesses = property(fget=weakness_list)

    def resistances_list(self):
        items = TypeChart.objects.filter(
            frm__name=self.name,
            ttype='resist')
        if items.exists():
            return self._build_dict(items)
        return []

    resistances = property(fget=resistances_list)

    def super_list(self):
        items = TypeChart.objects.filter(
            frm__name=self.name,
            ttype='super effective')
        if items.exists():
            return self._build_dict(items)
        return []

    supers = property(fget=super_list)

    def ineffective_list(self):
        items = TypeChart.objects.filter(
            frm__name=self.name,
            ttype='ineffective')
        if items.exists():
            return self._build_dict(items)
        return []

    ineffectives = property(fget=ineffective_list)

    def no_list(self):
        items = TypeChart.objects.filter(
            frm__name=self.name,
            ttype='noeffect')
        if items.exists():
            return self._build_dict(items)
        return []

    no_effects = property(fget=no_list)


class TypeChart(DateTimeModel):

    def __unicode__(self):
        return ' '.join([self.frm.name, self.ttype, 'against', self.to.name])

    frm = models.ForeignKey(
        Type, blank=True, null=True, related_name='type_frm')

    to = models.ForeignKey(
        Type, blank=True, null=True, related_name='type_to')

    TYPES = (
        ('weak', 'weak'),
        ('super effective', 'super effective'),
        ('resistant', 'resistant'),
        ('ineffective', 'ineffective'),
        ('noeffect', 'noeffect'),
        ('resist', 'resist'),
    )

    ttype = models.CharField(
        max_length=15, choices=TYPES, blank=True, null=True)


class EggGroup(DateTimeModel):

    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=50)

    def get_pokes(self):

        pokes = Pokemon.objects.filter(
            egg_group=self
        )

        lst = []
        if pokes.exists():
            for p in pokes:
                lst.append(dict(
                    name=p.name.capitalize(),
                    resource_uri='/api/v1/pokemon/' + str(p.pkdx_id) + '/'
                ))
        return lst

    pokemon = property(fget=get_pokes)


class Game(DateTimeModel):

    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=50)

    generation = models.IntegerField(max_length=4)

    release_year = models.IntegerField(max_length=6)


class Description(DateTimeModel):

    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=50)

    description = models.TextField(max_length=200)

    game = models.ManyToManyField(Game, blank=True, null=True)

    def get_game_details(self):
        lst = []
        for g in self.game.all():
            lst.append(dict(
                name=g.name,
                resource_uri='/api/v1/game/' + str(g.id) + '/')
            )
        return lst

    n_game = property(fget=get_game_details)

    def get_pokemon(self):

        nm = self.name.split('_')[0]

        pokes = Pokemon.objects.filter(
            name=nm.lower()
        )

        if pokes.exists():
            return dict(
                name=pokes[0].name,
                resource_uri='/api/v1/pokemon/' + str(pokes[0].pkdx_id) + '/')
        return []

    pokemon = property(fget=get_pokemon)


class Move(DateTimeModel):

    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=50)

    description = models.TextField(max_length=200)

    etype = models.ManyToManyField(Type, null=True)

    pp = models.IntegerField(max_length=5)

    CATEGORY = (
        ('physical', 'physical'),
        ('special', 'special'),
        ('status', 'status'),
    )

    category = models.CharField(choices=CATEGORY, max_length=10)

    power = models.IntegerField(max_length=6)

    accuracy = models.IntegerField(max_length=6)


class Sprite(DateTimeModel):

    def __unicode__(self):
            return self.name

    name = models.CharField(max_length=50)

    image = ProcessedImageField(
        [ResizeToFill(96, 96)],
        upload_to=unique_filename,
        format='PNG',
        options={'quality': 80})

    def get_pokemon(self):

        nm = self.name.split('_')[0]

        pokes = Pokemon.objects.filter(
            name=nm.lower()
        )

        if pokes.exists():
            return dict(
                name=pokes[0].name,
                resource_uri='/api/v1/pokemon/' + str(pokes[0].pkdx_id) + '/')
        return []

    pokemon = property(fget=get_pokemon)


class Pokemon(DateTimeModel):

    def __unicode__(self):
        return ' - '.join([str(self.pkdx_id), self.name])

    name = models.CharField(max_length=50)

    pkdx_id = models.IntegerField(max_length=4, blank=True)

    species = models.CharField(max_length=30)

    height = models.CharField(max_length=10)

    weight = models.CharField(max_length=10)

    ev_yield = models.CharField(max_length=20)

    catch_rate = models.IntegerField(max_length=4)

    happiness = models.IntegerField(max_length=4)

    exp = models.IntegerField(max_length=5)

    GROWTHS = (
        ('slow', 'slow'),
        ('medium slow', 'medium slow'),
        ('medium', 'medium'),
        ('medium fast', 'medium fast'),
        ('fast', 'fast'),
    )

    growth_rate = models.CharField(choices=GROWTHS, max_length=15)

    male_female_ratio = models.CharField(max_length=10)

    hp = models.IntegerField(max_length=4)

    attack = models.IntegerField(max_length=4)

    defense = models.IntegerField(max_length=4)

    sp_atk = models.IntegerField(max_length=4)

    sp_def = models.IntegerField(max_length=4)

    speed = models.IntegerField(max_length=4)

    total = models.IntegerField(max_length=6)

    egg_cycles = models.IntegerField(max_length=6)

    abilities = models.ManyToManyField(
        Ability, blank=True,  null=True)

    def ability_names(self):
        lst = []
        for a in self.abilities.all():
            lst.append(dict(
                resource_uri='/api/v1/ability/' + str(a.id) + '/',
                name=a.name.lower())
            )
        return lst

    ability_list = property(fget=ability_names)

    def get_evolution_details(self):

        evols = Evolution.objects.filter(
            frm=self
        )

        if evols.exists():
            lst = []
            for e in evols:
                d = dict(
                    to=e.to.name.capitalize(),
                    resource_uri='/api/v1/pokemon/' + str(e.to.pkdx_id) + '/',
                    method=e.method,
                )
                if e.level > 0:
                    d['level'] = e.level
                if e.detail:
                    d['detail'] = e.detail
                lst.append(d)
            return lst
        return []

    evolutions = property(fget=get_evolution_details)

    types = models.ManyToManyField(
        Type, blank=True,  null=True)

    def type_list(self):
        lst = []
        for t in self.types.all():
            lst.append(dict(
                resource_uri='/api/v1/type/' + str(t.id) + '/',
                name=t.name.lower())
            )
        return lst

    type_list = property(fget=type_list)

    egg_group = models.ManyToManyField(
        EggGroup, blank=True,  null=True)

    def get_eggs(self):

        lst = []
        for e in self.egg_group.all():
            lst.append(dict(
                name=e.name.capitalize(),
                resource_uri='/api/v1/egg/' + str(e.id) + '/'
            ))
        return lst

    eggs = property(fget=get_eggs)

    descriptions = models.ManyToManyField(
        Description, blank=True,  null=True)

    def get_sprites(self):
        lst = []
        for s in self.sprites.all():
            lst.append(dict(
                name=self.name,
                resource_uri='/api/v1/sprite/' + str(s.id) + '/')
            )
        return lst

    my_sprites = property(fget=get_sprites)

    sprites = models.ManyToManyField(
        Sprite, blank=True,  null=True)

    def get_moves(self):

        moves = MovePokemon.objects.filter(
            pokemon=self
        )

        lst = []
        if moves.exists():
            for m in moves:
                d = dict(
                    name=m.move.name.capitalize(),
                    resource_uri='/api/v1/move/' + str(m.move.id) + '/',
                    learn_type=m.learn_type
                )
                if m.level > 0:
                    d['level'] = m.level
                lst.append(d)
        return lst

    moves = property(fget=get_moves)


class Evolution(DateTimeModel):

    def __unicode__(self):
        return self.frm.name + ' to ' + self.to.name

    frm = models.ForeignKey(
        Pokemon, null=True, blank=True,
        related_name='frm_evol_pokemon')

    to = models.ForeignKey(
        Pokemon, null=True, blank=True,
        related_name='to_evol_pokemon')

    EVOLV_METHODS = (
        ('level up', 'level_up'),
        ('stone', 'stone'),
        ('trade', 'trade'),
        ('other', 'other'),
    )

    level = models.IntegerField(max_length=3, default=0)

    method = models.CharField(
        choices=EVOLV_METHODS, max_length=10, default=0)

    detail = models.CharField(max_length=10, null=True, blank=True)


class MovePokemon(DateTimeModel):

    def __unicode__(self):
        return self.pokemon.name + ' - ' + self.move.name

    pokemon = models.ForeignKey(
        Pokemon, related_name='move', null=True, blank=True)

    move = models.ForeignKey(
        Move, related_name='pokemon', null=True, blank=True)

    LEARN = (
        ('level up', 'level up'),
        ('machine', 'machine'),
        ('egg move', 'egg move'),
        ('tutor', 'tutor'),
        ('other', 'other'),
    )

    learn_type = models.CharField(
        choices=LEARN, max_length=15, default='level up')

    level = models.IntegerField(
        max_length=6, default=0, null=True, blank=True)


class Pokedex(DateTimeModel):

    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=60)

    def _all_pokes(self):
        lst = []
        for p in Pokemon.objects.all():
            lst.append(dict(
                name=p.name,
                resource_uri='api/v1/pokemon/' + str(p.pkdx_id) + '/'
            ))
        return lst

    pokemon = property(fget=_all_pokes)
