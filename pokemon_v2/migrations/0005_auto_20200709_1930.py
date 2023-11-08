from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pokemon_v2", "0004_iso639length_20191217"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pokemonsprites",
            name="sprites",
            field=models.CharField(max_length=20000),
        ),
    ]
