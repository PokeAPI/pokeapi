import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pokemon_v2", "0031_encounterpokemondetail"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pokemonevolution",
            name="time_of_day",
            field=models.CharField(blank=True, default="", max_length=10),
        ),
        migrations.AddField(
            model_name="pokemonformcondition",
            name="base_form",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="base_form_conditions",
                to="pokemon_v2.pokemonform",
            ),
        ),
    ]
