

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("pokemon_v2", "0012_auto_20220626_1402"),
    ]

    operations = [
        migrations.CreateModel(
            name="PokemonAbilityPast",
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
                ("is_hidden", models.BooleanField(default=False)),
                ("slot", models.IntegerField()),
                (
                    "generation",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pokemonabilitypast",
                        to="pokemon_v2.Generation",
                    ),
                ),
                (
                    "ability",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pokemonabilitypast",
                        to="pokemon_v2.Ability",
                    ),
                ),
                (
                    "pokemon",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pokemonabilitypast",
                        to="pokemon_v2.Pokemon",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
