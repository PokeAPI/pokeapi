from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pokemon_v2", "0010_pokemonformtype"),
    ]

    operations = [
        migrations.CreateModel(
            name="PokemonCries",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                 ),
                ("cries", models.CharField(max_length=500)),
                (
                    "pokemon_cry", models.ForeignKey(
                        on_delete=models.CASCADE,
                        related_name="pokemon",
                        blank=True,
                        to="pokemon_v2.PokemonSpecies",
                        null=True,
                    ),
                ),
            ],
            options={
                "abstract": False,
            }
        ),
    ]
