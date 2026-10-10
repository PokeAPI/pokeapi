import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pokemon_v2", "0034_item_cost_and_time_of_day"),
    ]

    operations = [
        migrations.CreateModel(
            name="PokemonFormFlavorText",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("flavor_text", models.CharField(max_length=500)),
                (
                    "language",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_language",
                        to="pokemon_v2.language",
                    ),
                ),
                (
                    "pokemon_form",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s",
                        to="pokemon_v2.pokemonform",
                    ),
                ),
                (
                    "version",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s",
                        to="pokemon_v2.version",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
