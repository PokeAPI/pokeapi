from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pokemon_v2", "0005_auto_20200709_1930"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pokemon",
            name="height",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="pokemon",
            name="weight",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="pokemon",
            name="base_experience",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
