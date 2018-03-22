#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
This is very, very ugly. PokeAPI V1 was built in one day when I didn't quite
understand how to process all this data, so it takes in a bunch of csv stuff
and dumps it into the models.

I used to go into the django shell and run these commands one at a time to
load the data into the database on prod. It took around 30-40 minutes to run
some of the scripts.

The builder for V2 will be exceptionally better than this.

So - if you want to see some of the worst code I've ever written, look below:

- Paul Hallett

"""

import csv

from pokemon.models import *


def build_pokes():
    file = open('data/v1/pokemon.csv', 'rb')

    rdr = csv.reader(file, delimiter=',')

    for row in rdr:
        if row[0] != 'id':
            new_p = Pokemon(
                pkdx_id=int(row[0]),
                name=str(row[1]),
                exp=int(row[5]),
                catch_rate=0,
                happiness=0,
                hp=0,
                attack=0,
                defense=0,
                speed=0,
                sp_atk=0,
                sp_def=0,
                total=0,
                egg_cycles=0,
            )
            new_p.save()
            print 'created pokemon %s' % new_p.name


def build_abilities():
    file = open('data/v1/abilities.csv', 'rb')

    rdr = csv.reader(file, delimiter=',')

    for row in rdr:
        if row[0] != 'id':
            new_a = Ability(
                name=row[1],
                description='',
            )
            new_a.save()
            print 'created ability %s' % new_a.name


def build_moves():
    file = open('data/v1/moves.csv', 'rb')

    rdr = csv.reader(file, delimiter=',')

    for row in rdr:
        if row[0] != 'id':
            new_a = Move(
                name=row[1],
                description='',
            )
            new_a.accuracy = row[6] if row[6] != '' else 0
            new_a.pp = row[5] if row[5] != '' else 0
            new_a.power = row[4] if row[4] != '' else 0
            new_a.save()
            print 'created move %s' % new_a.name


def build_ability_pokes():
    file = open('data/v1/ability_pokes.csv', 'rb')

    rdr = csv.reader(file, delimiter=',')

    for row in rdr:
        if row[0] != 'pokemon_id':
            poke = Pokemon.objects.filter(pkdx_id=row[0])[0]
            ab = Ability.objects.get(pk=int(row[1]))

            poke.abilities.add(ab)
            poke.save()
            print 'added ' + ab.name + ' to ' + poke.name


def build_move_pokes():
    file = open('data/v1/poke_moves.csv', 'rb')

    rdr = csv.reader(file, delimiter=',')

    LEARN = ['', 'level up', 'egg move', 'tutor', 'machine', 'other']

    for row in rdr:
        if row[0] != 'pokemon_id':
            poke = Pokemon.objects.filter(pkdx_id=row[0])[0]
            mv = Move.objects.get(pk=int(row[2]))

            pm, created = MovePokemon.objects.get_or_create(
                pokemon=poke,
                move=mv,
            )
            if created:
                learn = LEARN[int(row[3])]if int(row[3]) <= 5 else LEARN[5]
                pm.learn_type = learn
                pm.level = row[4] if row[4] != '' else 0
                pm.save()
                print 'added ' + pm.__unicode__()


def build_egg_pokes():
    file = open('data/v1/pokes_eggs.csv', 'rb')

    rdr = csv.reader(file, delimiter=',')

    for row in rdr:
        if row[0] != 'species_id':
            poke = Pokemon.objects.filter(pkdx_id=row[0])[0]
            egg = EggGroup.objects.get(pk=int(row[1]))

            poke.egg_group.add(egg)
            poke.save()
            # print 'added ' + egg.name + ' to ' + poke.name


def build_type_pokes():
    file = open('data/v1/poke_types.csv', 'rb')

    rdr = csv.reader(file, delimiter=',')

    for row in rdr:
        if row[0] != 'pokemon_id':
            poke = Pokemon.objects.filter(pkdx_id=row[0])[0]
            ty = Type.objects.get(pk=int(row[1]))

            poke.types.add(ty)
            poke.save()
            print 'added ' + ty.name + ' to ' + poke.name


def build_sprites():

    for i in range(1, 719):
        str_num = str(i)
        sfile = 'img/%s.png' % str_num
        p = Pokemon.objects.filter(pkdx_id=i)
        if p.exists():
            p = p[0]
            s = Sprite(
                name=p.name + '_auto',
                image=sfile)
            s.save()
            print 'built sprite for %s' % p.name
        else:
            print 'pokemon sprite with id %d does not exist' % i


def poke_sprite_links():
    for i in Sprite.objects.all():
        p = Pokemon.objects.filter(name=i.name[:-5])
        if p.exists():
            p = p[0]
            p.sprites.add(i)
            p.save()
            print 'Sprite added to pokemon %s' % p.name
        else:
            print '%s pokemon does not exist' % i.name[:-5]


def build_poke_stats():
    """
    Get each Pokemon and build stats for it from two seperate files.
    """
    file = open('data/v1/pokemon.csv', 'rb')

    rdr = csv.reader(file, delimiter=',')

    for row in rdr:
        if row[0] != 'id':
            p = Pokemon.objects.filter(pkdx_id=row[0])
            if p.exists():
                p = p[0]
                p.height = row[3] if row[3] != '' else 0
                p.weight = row[4] if row[4] != '' else 0
                p.happiness = row[5] if row[5] != '' else 0
                p.save()
                print 'built stats for %s' % p.name

    file = open('data/v1/pokemon_stats.csv')

    rdr = csv.reader(file, delimiter=',')

    for row in rdr:
        if row[0] != 'pokemon_id':
            p = Pokemon.objects.filter(pkdx_id=row[0])
            if p.exists():
                p = p[0]
                if row[1] == '1':
                    p.hp = row[2]
                if row[1] == '2':
                    p.attack = row[2]
                if row[1] == '3':
                    p.defense = row[2]
                if row[1] == '4':
                    p.sp_atk = row[2]
                if row[1] == '5':
                    p.sp_def = row[2]
                if row[1] == '6':
                    p.speed = row[2]
            p.save()
            print 'stat for %s added' % p.name


def build_evolutions():
    """
    Build all the evolution links
    """

    file = open('data/v1/evolutions.csv', 'rb')

    rdr = csv.reader(file, delimiter=',')

    method = [' ', 'level_up', 'trade', 'stone', 'other']

    for row in rdr:
        if row[0] != 'id':
            frm = Pokemon.objects.filter(pkdx_id=int(row[1])-1)
            if not frm.exists():
                frm = Pokemon.objects.filter(pkdx_id=1)[0]
            else:
                frm = frm[0]
            to = Pokemon.objects.filter(pkdx_id=int(row[1]))
            if not to.exists():
                to = Pokemon.objects.filter(pkdx_id=2)[0]
            else:
                to = to[0]
            if method[int(row[2])] == 'level_up':
                e = Evolution(
                    frm=frm,
                    to=to,
                    method=method[int(row[2])],
                    level=row[4] if row[4] != '' else 0
                )

                e.save()
                print 'created link %s' % e.__unicode__()


def build_move_descriptions():
    """
        Build all the move descriptions
    """

    for m in Move.objects.all():
        f_moves = open('data/moves.csv', 'rb')
        f_descrips = open('data/move_effects.csv', 'rb')
        for row in csv.reader(f_moves, delimiter=','):
            if str(row[1]) == m.name:
                for drow in csv.reader(f_descrips, delimiter=','):
                    if str(row[10]) == str(drow[0]):
                        s = str(drow[3]).replace(
                            '$effect_chance', str(row[11]))
                        s = s.replace('[', '')
                        s = s.replace(']', '')
                        m.description = s
                        m.save()
                        print 'added description to %s' % m.name


def build_complex_evolutions():
    """
    Build complex evolutions from a better list
    """

    fspecies = open('data/v1/species.csv', 'rb')
    fevols = open('data/v1/evolutions.csv', 'rb')

    method = [' ', 'level_up', 'trade', 'stone', 'other']
    c = 0
    for row in csv.reader(fspecies, delimiter=','):
        if row[0] != 'id' and row[3] != '':
            frm = Pokemon.objects.get(pkdx_id=int(row[3]))
            fevols = open('data/v1/evolutions.csv', 'rb')
            for erow in csv.reader(fevols, delimiter=','):
                if erow[0] != 'id':
                    to = Pokemon.objects.get(pkdx_id=int(erow[1]))
                    if int(erow[1]) == int(row[0]):
                        mthd = method[int(erow[2])]
                        lvl = erow[4] if erow[4] != '' else 0
                        e = Evolution(frm=frm, to=to, method=mthd, level=lvl)
                        e.save()
                        print 'created evolution from %s to %s' % (frm.name, to.name)
                        c += 1

    print '%s created' % str(c)


def build_pokedex_descriptions():
    """
    Build the pokedex descriptions for Pokemon
    """

    gens = {1: '1', 2: '1', 3: '1', 4: '1', 5: '1', 6: '1',
            7: '2', 8: '2', 9: '2', 10: '3', 11: '3', 12: '3', 13: '3',
            14: '3', 15: '4', 16: '4', 17: '4', 18: '4', 19: '4', 20: '5',
            21: '5', 22: '5', 23: '6', 24: '6'}

    descrips = open('data/v1/pokedex_descriptions.csv', 'rb')
    c = 0
    for row in csv.reader(descrips, delimiter=','):
        if row[0] != 'species_id' and int(row[2]) == 9:
            p = Pokemon.objects.get(pkdx_id=int(row[0]))
            g = Game.objects.get(pk=row[1])
            d, _ = Description.objects.get_or_create(
                name=p.name+'_gen_'+gens[int(row[1])],
                description=row[3])
            d.game.add(g)
            d.save()
            print 'Description %s created, %s added' % (d.name, g.name)
            c += 1

    print 'made %s descriptions' % str(c)
