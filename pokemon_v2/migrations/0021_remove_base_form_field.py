# Generated migration to remove base_form field from PokemonEvolution

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("pokemon_v2", "0020_add_regional_evolution_fields"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="pokemonevolution",
            name="base_form",
        ),
    ]
