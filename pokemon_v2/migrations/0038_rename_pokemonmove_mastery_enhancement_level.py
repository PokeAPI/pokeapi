from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("pokemon_v2", "0037_evolutionvariable_source"),
    ]

    operations = [
        migrations.RenameField(
            model_name="pokemonmove",
            old_name="mastery",
            new_name="enhancement_level",
        ),
    ]
