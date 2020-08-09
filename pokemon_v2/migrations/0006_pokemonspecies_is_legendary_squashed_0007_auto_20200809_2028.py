# Generated by Django 2.1.11 on 2020-08-09 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [
        ("pokemon_v2", "0006_pokemonspecies_is_legendary"),
        ("pokemon_v2", "0007_auto_20200809_2028"),
    ]

    dependencies = [
        ("pokemon_v2", "0005_auto_20200709_1930"),
    ]

    operations = [
        migrations.AddField(
            model_name="pokemonspecies",
            name="is_legendary",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="pokemonspecies",
            name="is_mythical",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="pokemonspecies",
            name="is_ultra_beast",
            field=models.BooleanField(default=False),
        ),
    ]