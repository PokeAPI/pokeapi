from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ("pokemon_v2", "0003_auto_20160530_1132"),
    ]

    operations = [
        migrations.AlterField(
            model_name="language",
            name="iso639",
            field=models.CharField(max_length=10),
            preserve_default=True,
        ),
    ]
