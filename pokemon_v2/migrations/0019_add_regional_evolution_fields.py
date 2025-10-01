# Generated migration for regional evolution metadata

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("pokemon_v2", "0018_auto_20250123_1838"),
    ]

    operations = [
        migrations.AddField(
            model_name="pokemonevolution",
            name="region",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="pokemon_v2.Region",
                help_text="Region where this evolution can occur (null = any region)",
            ),
        ),
        migrations.AddField(
            model_name="pokemonevolution",
            name="base_form",
            field=models.ForeignKey(
                blank=True,
                null=True,
                related_name="base_form_evolutions",
                on_delete=django.db.models.deletion.CASCADE,
                to="pokemon_v2.PokemonSpecies",
                help_text="Specific form required for evolution (null = any form)",
            ),
        ),
    ]
